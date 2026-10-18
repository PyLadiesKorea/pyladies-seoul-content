import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "notify-web-pr.yml"
REPOSITORY = "PyLadiesKorea/pyladies-seoul-content"
HEAD_SHA = "0123456789abcdef" * 2 + "01234567"


def workflow_run_script() -> str:
    lines = WORKFLOW_PATH.read_text(encoding="utf-8").splitlines()
    marker_index = next(
        index for index, line in enumerate(lines) if line.strip() == "run: |"
    )
    marker_indent = len(lines[marker_index]) - len(lines[marker_index].lstrip())
    body = []
    for line in lines[marker_index + 1 :]:
        if line.strip() and len(line) - len(line.lstrip()) <= marker_indent:
            break
        body.append(line)
    return textwrap.dedent("\n".join(body))


class NotifyWebPrWorkflowTests(unittest.TestCase):
    def run_dispatch(self, **overrides):
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
                    "GH_TOKEN": "test-token",
                    "GITHUB_EVENT_NAME": "pull_request_target",
                    "GITHUB_REPOSITORY": REPOSITORY,
                    "GITHUB_SHA": "a" * 40,
                    "PR_ACTION": "opened",
                    "PR_STATE": "open",
                    "PR_HEAD_REPOSITORY": REPOSITORY,
                    "PR_BASE_REPOSITORY": REPOSITORY,
                    "PR_BASE_REF": "dev",
                    "CONTENT_PR": "17",
                    "PR_HEAD_SHA": HEAD_SHA,
                    "PATH": f"{temporary_path}:{environment['PATH']}",
                }
            )
            environment.update(overrides)
            result = subprocess.run(
                ["bash", "-c", workflow_run_script()],
                cwd=temporary_path,
                env=environment,
                capture_output=True,
                check=False,
                text=True,
            )
            self.assertFalse((temporary_path / "injected").exists())
            payload = (
                json.loads(payload_path.read_text(encoding="utf-8"))
                if payload_path.exists()
                else None
            )
            arguments = (
                arguments_path.read_text(encoding="utf-8").splitlines()
                if arguments_path.exists()
                else None
            )
            return result, payload, arguments

    def test_supported_events_dispatch_exact_pr_head_not_target_sha(self):
        for base in ("main", "dev"):
            for action in ("opened", "synchronize", "reopened", "edited", "ready_for_review"):
                with self.subTest(base=base, action=action):
                    result, payload, arguments = self.run_dispatch(
                        PR_BASE_REF=base, PR_ACTION=action
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(
                        payload,
                        {
                            "event_type": "content-pr-updated",
                            "client_payload": {"content_pr": 17, "content_commit": HEAD_SHA},
                        },
                    )
                    self.assertEqual(
                        arguments,
                        [
                            "api", "--method", "POST", "--header",
                            "X-GitHub-Api-Version: 2022-11-28", "--input", "-",
                            "repos/PyLadiesKorea/pyladies-seoul-web/dispatches",
                        ],
                    )

    def test_fork_skips_without_requiring_token(self):
        result, payload, arguments = self.run_dispatch(
            PR_HEAD_REPOSITORY="someone/fork", GH_TOKEN=""
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skipping fork PR", result.stdout)
        self.assertIsNone(payload)
        self.assertIsNone(arguments)

    def test_invalid_event_metadata_never_dispatches(self):
        invalid_metadata = (
            {"GITHUB_EVENT_NAME": "pull_request"},
            {"GITHUB_EVENT_NAME": "push"},
            {"PR_ACTION": "closed"},
            {"PR_STATE": "closed"},
            {"GITHUB_REPOSITORY": "someone/fork"},
            {"PR_BASE_REPOSITORY": "someone/fork"},
            {"PR_BASE_REF": "feature/something"},
            {"PR_BASE_REF": "refs/heads/dev"},
            {"PR_BASE_REF": "dev; touch injected"},
            {"PR_HEAD_SHA": ""},
            {"PR_HEAD_SHA": "abc123"},
            {"PR_HEAD_SHA": "refs/heads/main"},
            {"PR_HEAD_SHA": "g" * 40},
            {"PR_HEAD_SHA": HEAD_SHA + "\n"},
            {"PR_HEAD_SHA": '$(touch injected)'},
            {"CONTENT_PR": ""},
            {"CONTENT_PR": "0"},
            {"CONTENT_PR": "-1"},
            {"CONTENT_PR": "01"},
            {"CONTENT_PR": "1.5"},
            {"CONTENT_PR": '17,"injected":true'},
            {"CONTENT_PR": '$(touch injected)'},
            {"GH_TOKEN": ""},
        )
        for overrides in invalid_metadata:
            with self.subTest(overrides=overrides):
                result, payload, arguments = self.run_dispatch(**overrides)
                self.assertNotEqual(result.returncode, 0)
                self.assertIsNone(payload)
                self.assertIsNone(arguments)


if __name__ == "__main__":
    unittest.main()
