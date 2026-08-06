import io
import tempfile
import unittest
from pathlib import Path

from scripts.validate_content_schema import run_validation, scan_event_bundles


class EventContentSchemaValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def make_bundle(self, name, *, korean_file=True):
        bundle = self.root / "events" / name
        bundle.mkdir(parents=True)
        if korean_file:
            (bundle / "ko.md").write_text("행사 본문\n", encoding="utf-8")
        return bundle

    def test_accepts_valid_event_bundle(self):
        self.make_bundle("20260806-python-workshop")

        self.assertEqual(scan_event_bundles(self.root), [])

    def test_rejects_each_invalid_direct_event_folder_name(self):
        invalid_names = (
            "2026-08-06-python-workshop",
            "20260806-Python-workshop",
            "20260806-python_workshop",
            "20260806-python-workshop-",
            "python-workshop",
        )
        for name in invalid_names:
            self.make_bundle(name)

        violations = scan_event_bundles(self.root)

        self.assertEqual(len(violations), len(invalid_names))
        self.assertEqual(
            {item.path.as_posix() for item in violations},
            {f"events/{name}" for name in invalid_names},
        )
        self.assertEqual(
            {item.reason for item in violations},
            {"invalid-event-slug"},
        )

    def test_requires_korean_markdown_in_each_event_bundle(self):
        self.make_bundle("20260806-python-workshop", korean_file=False)

        violations = scan_event_bundles(self.root)

        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].rule_id, "CONTENT-SCHEMA-001")
        self.assertEqual(
            violations[0].path,
            Path("events/20260806-python-workshop/ko.md"),
        )
        self.assertEqual(violations[0].reason, "missing-ko-md")

    def test_only_checks_direct_event_directories(self):
        bundle = self.make_bundle("20260806-python-workshop")
        (bundle / "Nested_Invalid_Name").mkdir()
        events = self.root / "events"
        (events / "Not_A_Directory.md").write_text("본문\n", encoding="utf-8")

        self.assertEqual(scan_event_bundles(self.root), [])

    def test_reports_rule_and_path_and_returns_failure(self):
        self.make_bundle("invalid-folder", korean_file=False)
        output = io.StringIO()

        exit_code = run_validation(self.root, stream=output)
        rendered = output.getvalue()

        self.assertEqual(exit_code, 1)
        self.assertEqual(rendered.count("CONTENT-SCHEMA-001"), 2)
        self.assertIn("events/invalid-folder", rendered)
        self.assertIn("events/invalid-folder/ko.md", rendered)


class CurrentRepositorySchemaTests(unittest.TestCase):
    def test_all_current_event_bundles_match_the_schema(self):
        repository_root = Path(__file__).resolve().parent.parent

        self.assertEqual(scan_event_bundles(repository_root), [])

    def test_validation_workflow_runs_the_schema_scan(self):
        repository_root = Path(__file__).resolve().parent.parent
        workflow = (
            repository_root / ".github" / "workflows" / "validate-content.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python scripts/validate_content_schema.py .", workflow)


if __name__ == "__main__":
    unittest.main()
