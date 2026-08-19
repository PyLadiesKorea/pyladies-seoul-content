#!/usr/bin/env python3
"""Reject personal contact data from public content Markdown bundles."""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TextIO

ALLOWED_ORGANIZATION_EMAILS = frozenset(
    {
        "coc@pyladies.com",
        "conduct-wg@python.org",
        "seoul@pyladies.com",
    }
)
PUBLIC_CONTENT_DIRECTORIES = (
    "about",
    "events",
    "members",
    "stories",
    "thanks",
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)
PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:"
    r"(?:01[016789]|02|0(?:3[1-3]|4[1-4]|5[1-5]|6[1-4]|70))"
    r"|\+82[ -]?(?:10|2|3[1-3]|4[1-4]|5[1-5]|6[1-4]|70)"
    r")"
    r"[ -]?\d{3,4}[ -]?\d{4}"
    r"(?!\d)"
)


@dataclass(frozen=True)
class Violation:
    rule_id: str
    path: Path
    line_number: int


def markdown_files(root: Path) -> Iterable[Path]:
    for directory_name in PUBLIC_CONTENT_DIRECTORIES:
        content_directory = root / directory_name
        if not content_directory.is_dir():
            continue
        for path in sorted(content_directory.rglob("*.md")):
            if ".git" not in path.parts:
                yield path


def scan_line(path: Path, line_number: int, line: str) -> list[Violation]:
    violations = []
    emails = {match.group(0).lower() for match in EMAIL_PATTERN.finditer(line)}
    if emails - ALLOWED_ORGANIZATION_EMAILS:
        violations.append(Violation("CONTENT-PII-001", path, line_number))
    if PHONE_PATTERN.search(line):
        violations.append(Violation("CONTENT-PII-002", path, line_number))
    return violations


def scan_tree(root: Path) -> list[Violation]:
    root = root.resolve()
    violations = []
    for path in markdown_files(root):
        relative_path = path.relative_to(root)
        with path.open(encoding="utf-8") as content_file:
            for line_number, line in enumerate(content_file, start=1):
                violations.extend(scan_line(relative_path, line_number, line))
    return violations


def run_validation(root: Path, stream: TextIO = sys.stdout) -> int:
    violations = scan_tree(root)
    if not violations:
        print("Content privacy validation passed.", file=stream)
        return 0

    print(f"Content privacy validation failed: {len(violations)} violation(s).", file=stream)
    for violation in violations:
        print(
            f"{violation.rule_id} {violation.path}:{violation.line_number}",
            file=stream,
        )
    print("Sensitive source text is intentionally omitted.", file=stream)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Repository root to scan (default: current directory)",
    )
    args = parser.parse_args()
    return run_validation(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
