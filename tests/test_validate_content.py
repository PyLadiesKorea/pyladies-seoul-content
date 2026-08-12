import io
import tempfile
import unittest
from pathlib import Path

from scripts.validate_content import run_validation, scan_tree


class ContentPrivacyValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_markdown(self, relative_path, content):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_allows_reviewed_organization_contacts(self):
        for category in ("about", "events", "members", "stories", "thanks"):
            self.write_markdown(
                f"{category}/official/ko.md",
                "\n".join(
                    (
                        "seoul@pyladies.com",
                        "coc@pyladies.com",
                        "conduct-wg@python.org",
                    )
                ),
            )

        self.assertEqual(scan_tree(self.root), [])

    def test_rejects_personal_email_in_every_public_content_category(self):
        categories = ("about", "events", "members", "stories", "thanks")
        for category in categories:
            self.write_markdown(f"{category}/example/ko.md", "person@example.com")

        violations = scan_tree(self.root)

        self.assertEqual(
            [item.rule_id for item in violations],
            ["CONTENT-PII-001"] * len(categories),
        )
        self.assertEqual(
            {item.path.parts[0] for item in violations},
            set(categories),
        )

    def test_rejects_unreviewed_email_on_an_allowed_domain(self):
        self.write_markdown("events/example/ko.md", "person@pyladies.com")

        violations = scan_tree(self.root)

        self.assertEqual([item.rule_id for item in violations], ["CONTENT-PII-001"])

    def test_rejects_phone_number_in_every_public_content_category(self):
        categories = ("about", "events", "members", "stories", "thanks")
        for category in categories:
            self.write_markdown(f"{category}/example/ko.md", "010-1234-5678")

        violations = scan_tree(self.root)

        self.assertEqual(
            [item.rule_id for item in violations],
            ["CONTENT-PII-002"] * len(categories),
        )
        self.assertEqual(
            {item.path.parts[0] for item in violations},
            set(categories),
        )

    def test_rejects_phone_numbers_with_or_without_separators(self):
        self.write_markdown(
            "members/example/ko.md",
            "\n".join(
                (
                    "010-1234-5678",
                    "0212345678",
                    "010 9876 5432",
                    "031-123-4567",
                    "070-1234-5678",
                    "+82 10-1234-5678",
                    "+82-2-1234-5678",
                )
            ),
        )

        violations = scan_tree(self.root)

        self.assertEqual(
            [item.rule_id for item in violations],
            ["CONTENT-PII-002"] * 7,
        )

    def test_allows_intentionally_published_names_and_payment_details(self):
        for category in ("events", "thanks"):
            self.write_markdown(
                f"{category}/example/ko.md",
                "\n".join(
                    (
                        "name: 공개 동의를 받은 표시 이름",
                        "입금 계좌: 공개은행 123-456-7890",
                    )
                ),
            )

        self.assertEqual(scan_tree(self.root), [])

    def test_failure_output_does_not_echo_detected_values(self):
        personal_email = "person@example.com"
        phone_number = "010-1234-5678"
        self.write_markdown(
            "members/example/ko.md",
            f"{personal_email}\n{phone_number}\n",
        )
        output = io.StringIO()

        exit_code = run_validation(self.root, stream=output)
        rendered = output.getvalue()

        self.assertEqual(exit_code, 1)
        self.assertIn("CONTENT-PII-001", rendered)
        self.assertIn("CONTENT-PII-002", rendered)
        self.assertNotIn(personal_email, rendered)
        self.assertNotIn(phone_number, rendered)

    def test_ignores_non_markdown_and_git_files(self):
        self.write_markdown("members/example/ko.md", "Safe public member")
        member_directory = self.root / "members" / "example"
        (member_directory / "cover.txt").write_text(
            "person@example.com", encoding="utf-8"
        )
        self.write_markdown("members/.git/cache.md", "person@example.com")

        self.assertEqual(scan_tree(self.root), [])

    def test_ignores_supporting_docs_outside_public_content_roots(self):
        self.write_markdown("docs/policy.md", "계좌번호를 공개하지 않습니다.")
        self.write_markdown("README.md", "Contact person@example.com in examples.")

        self.assertEqual(scan_tree(self.root), [])


if __name__ == "__main__":
    unittest.main()
