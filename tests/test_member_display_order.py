import unittest
from pathlib import Path


APPROVED_MEMBER_ORDER = [
    "윤수진",
    "차화영",
    "백찬희",
    "최혜림",
    "최예리",
]


def member_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", 2)
    values = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def listed_members(repository_root):
    members = []
    for path in sorted((repository_root / "members").glob("*/ko.md")):
        frontmatter = member_frontmatter(path)
        if frontmatter.get("listed", "true").lower() == "false":
            continue
        members.append(frontmatter)
    return members


class CurrentMemberDisplayOrderTests(unittest.TestCase):
    def setUp(self):
        self.repository_root = Path(__file__).resolve().parent.parent
        self.members = listed_members(self.repository_root)

    def test_listed_members_have_unique_consecutive_positive_orders(self):
        orders = [int(member["order"]) for member in self.members]

        self.assertEqual(sorted(orders), list(range(1, len(orders) + 1)))

    def test_listed_members_match_the_approved_global_order(self):
        ordered_names = [
            member["name"]
            for member in sorted(
                self.members,
                key=lambda member: (int(member["order"]), member["name"]),
            )
        ]

        self.assertEqual(ordered_names, APPROVED_MEMBER_ORDER)


if __name__ == "__main__":
    unittest.main()
