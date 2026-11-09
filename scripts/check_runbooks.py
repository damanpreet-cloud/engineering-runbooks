#!/usr/bin/env python3
"""Fail if any runbook is missing a required section or review metadata."""

import pathlib
import sys

REQUIRED_HEADINGS = [
    "## Summary",
    "## Severity",
    "## Detection",
    "## Impact",
    "## Diagnosis",
    "## Mitigation",
    "## Escalation",
    "## Verification",
    "## Prevention",
]
REQUIRED_METADATA = ["Owner:", "Last reviewed:"]


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    failures = []
    for path in sorted((root / "runbooks").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                failures.append(f"{path.name}: missing '{heading}'")
        for key in REQUIRED_METADATA:
            if key not in text:
                failures.append(f"{path.name}: missing '{key}'")
    if failures:
        print("\n".join(failures))
        return 1
    print("All runbooks have the required sections.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
