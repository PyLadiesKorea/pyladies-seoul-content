#!/usr/bin/env python3
"""Validate the minimal filesystem schema for public event bundles."""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TextIO

EVENTS_DIRECTORY = "events"
EVENT_BUNDLE_PATTERN = re.compile(
    r"^[0-9]{8}-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
RULE_ID = "CONTENT-SCHEMA-001"


@dataclass(frozen=True)
class SchemaViolation:
    rule_id: str
    path: Path
    reason: str


def event_bundle_directories(root: Path) -> Iterable[Path]:
    events_directory = root / EVENTS_DIRECTORY
    if not events_directory.is_dir():
        return
    for path in sorted(events_directory.iterdir(), key=lambda item: item.name):
        if path.is_dir():
            yield path


def scan_event_bundles(root: Path) -> list[SchemaViolation]:
    root = root.resolve()
    violations = []
    for bundle in event_bundle_directories(root):
        relative_bundle = bundle.relative_to(root)
        if EVENT_BUNDLE_PATTERN.fullmatch(bundle.name) is None:
            violations.append(
                SchemaViolation(RULE_ID, relative_bundle, "invalid-event-slug")
            )

        korean_file = bundle / "ko.md"
        if not korean_file.is_file():
            violations.append(
                SchemaViolation(
                    RULE_ID,
                    korean_file.relative_to(root),
                    "missing-ko-md",
                )
            )
    return violations


def run_validation(root: Path, stream: TextIO = sys.stdout) -> int:
    root = root.resolve()
    bundles = list(event_bundle_directories(root))
    violations = scan_event_bundles(root)
    if not violations:
        print(
            f"Content schema validation passed: {len(bundles)} event bundle(s).",
            file=stream,
        )
        return 0

    print(
        f"Content schema validation failed: {len(violations)} violation(s).",
        file=stream,
    )
    for violation in violations:
        print(
            f"{violation.rule_id} {violation.path} {violation.reason}",
            file=stream,
        )
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
