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
    def run_dispatch(self, *, token: str, commit: str, branch: str):
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
                    "GITHUB_REF_NAME": branch,
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

    def test_workflow_triggers_main_and_dev_pushes(self):
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("branches: [main, dev]", workflow)

    def test_main_dispatches_prod_event_with_exact_content_commit(self):
        commit = "0123456789abcdef" * 2 + "01234567"

        result, payload, arguments = self.run_dispatch(
            token="test-token", commit=commit, branch="main"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            payload,
            {
                "event_type": "content-updated",
                "client_payload": {"content_commit": commit},
            },
        )
        self.assertNotEqual(payload["event_type"], "content-dev-updated")
        self.assertIn("repos/PyLadiesKorea/pyladies-seoul-web/dispatches", arguments)

    def test_dev_dispatches_dev_event_with_exact_content_commit(self):
        commit = "89abcdef0123456789abcdef0123456789abcdef"

        result, payload, arguments = self.run_dispatch(
            token="test-token", commit=commit, branch="dev"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            payload,
            {
                "event_type": "content-dev-updated",
                "client_payload": {"content_commit": commit},
            },
        )
        self.assertNotEqual(payload["event_type"], "content-updated")
        self.assertIn("repos/PyLadiesKorea/pyladies-seoul-web/dispatches", arguments)

    def test_missing_token_fails_before_calling_github(self):
        commit = "0123456789abcdef" * 2 + "01234567"

        result, payload, arguments = self.run_dispatch(
            token="", commit=commit, branch="main"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("WEB_DISPATCH_TOKEN is not configured", result.stdout)
        self.assertIsNone(payload)
        self.assertIsNone(arguments)

    def test_non_full_commit_sha_fails_before_calling_github(self):
        result, payload, arguments = self.run_dispatch(
            token="test-token", commit="abc123", branch="dev"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GITHUB_SHA must be a 40-character commit SHA", result.stdout)
        self.assertIsNone(payload)
        self.assertIsNone(arguments)

    def test_unknown_or_missing_branch_fails_before_calling_github(self):
        commit = "0123456789abcdef" * 2 + "01234567"

        for branch in ("feature/example", ""):
            with self.subTest(branch=branch):
                result, payload, arguments = self.run_dispatch(
                    token="test-token", commit=commit, branch=branch
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Unsupported content branch", result.stdout)
                self.assertIsNone(payload)
                self.assertIsNone(arguments)

    def test_token_is_not_exposed_in_payload_arguments_or_output(self):
        token = "distinct-secret-token-value"
        commit = "0123456789abcdef" * 2 + "01234567"

        result, payload, arguments = self.run_dispatch(
            token=token, commit=commit, branch="main"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(token, json.dumps(payload))
        self.assertNotIn(token, "\n".join(arguments))
        self.assertNotIn(token, result.stdout)
        self.assertNotIn(token, result.stderr)

    def test_token_is_not_exposed_when_validation_fails(self):
        token = "distinct-secret-token-value"

        result, payload, arguments = self.run_dispatch(
            token=token, commit="invalid-sha", branch="dev"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(token, result.stdout)
        self.assertNotIn(token, result.stderr)
        self.assertIsNone(payload)
        self.assertIsNone(arguments)

    def test_dispatch_contract_documents_environment_mapping_and_activation(self):
        contract = CONTRACT_PATH.read_text(encoding="utf-8")

        for requirement_id in ("CD-001", "CD-002", "CD-003", "CD-004"):
            self.assertIn(requirement_id, contract)

        self.assertIn("`main` push는 `event_type: content-updated`", contract)
        self.assertIn("`dev` push는 `event_type: content-dev-updated`", contract)
        self.assertIn("client_payload.content_commit", contract)
        self.assertIn("default branch", contract)
        self.assertIn("merge push 자체", contract)


if __name__ == "__main__":
    unittest.main()
