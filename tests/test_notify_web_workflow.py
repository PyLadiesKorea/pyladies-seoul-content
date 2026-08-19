import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "notify-web.yml"
CONTRACT_PATH = REPOSITORY_ROOT / "docs" / "CONTENT_DISPATCH.md"


def workflow_run_script() -> str:
    lines = WORKFLOW_PATH.read_text(encoding="utf-8").splitlines()
    marker_index = next(
        index for index, line in enumerate(lines) if line.strip() == "run: |"
    )
    marker_indent = len(lines[marker_index]) - len(lines[marker_index].lstrip())
    body = []

    for line in lines[marker_index + 1 :]:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            if indent <= marker_indent:
                break
        body.append(line)

    return textwrap.dedent("\n".join(body))


class NotifyWebWorkflowTests(unittest.TestCase):
    def run_dispatch(self, *, token: str, commit: str):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            fake_gh = temporary_path / "gh"
            payload_path = temporary_path / "payload.json"
            arguments_path = temporary_path / "arguments.txt"
            fake_gh.write_text(
                "#!/bin/sh\n"
                'cat > "$CAPTURE_PAYLOAD"\n'
                'printf "%s\\n" "$@" > "$CAPTURE_ARGUMENTS"\n',
                encoding="utf-8",
            )
            fake_gh.chmod(0o755)

            environment = os.environ.copy()
            environment.update(
                {
                    "CAPTURE_ARGUMENTS": str(arguments_path),
                    "CAPTURE_PAYLOAD": str(payload_path),
                    "GH_TOKEN": token,
                    "GITHUB_SHA": commit,
                    "PATH": f"{temporary_path}:{environment['PATH']}",
                }
            )
            result = subprocess.run(
                ["bash", "-c", workflow_run_script()],
                cwd=REPOSITORY_ROOT,
                env=environment,
                capture_output=True,
                check=False,
                text=True,
            )

            payload = None
            if payload_path.exists():
                payload = json.loads(payload_path.read_text(encoding="utf-8"))

            arguments = None
            if arguments_path.exists():
                arguments = arguments_path.read_text(encoding="utf-8").splitlines()

            return result, payload, arguments

    def test_dispatch_payload_includes_exact_content_commit(self):
        commit = "0123456789abcdef" * 2 + "01234567"

        result, payload, arguments = self.run_dispatch(
            token="test-token", commit=commit
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            payload,
            {
                "event_type": "content-updated",
                "client_payload": {"content_commit": commit},
            },
        )
        self.assertIn(
            "repos/PyLadiesKorea/pyladies-seoul-web/dispatches", arguments
        )

    def test_missing_token_fails_before_calling_github(self):
        commit = "0123456789abcdef" * 2 + "01234567"

        result, payload, arguments = self.run_dispatch(token="", commit=commit)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("WEB_DISPATCH_TOKEN is not configured", result.stdout)
        self.assertIsNone(payload)
        self.assertIsNone(arguments)

    def test_non_full_commit_sha_fails_before_calling_github(self):
        result, payload, arguments = self.run_dispatch(
            token="test-token", commit="abc123"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GITHUB_SHA must be a 40-character commit SHA", result.stdout)
        self.assertIsNone(payload)
        self.assertIsNone(arguments)

    def test_dispatch_contract_documents_default_branch_limitation(self):
        contract = CONTRACT_PATH.read_text(encoding="utf-8")

        self.assertIn("client_payload.content_commit", contract)
        self.assertIn("40", contract)
        self.assertIn("default branch", contract)
        self.assertIn(".github/workflows/deploy.yml", contract)


if __name__ == "__main__":
    unittest.main()
