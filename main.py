#!/usr/bin/env python3
"""Write one fortune cookie message for a software engineer to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The fortune is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 120 characters, not only white space.
"""

import os
import sys
from pathlib import Path

FORTUNE = "You will finally fix the bug today by deleting the feature nobody used."

MIN_CHARS = 1
MAX_CHARS = 120
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 120 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"fortune is {chars} characters, outside 1-120")
    if not text.strip():
        raise ValueError("fortune is only white space")
    if "\n" in text:
        raise ValueError("fortune must be a single line")
    return chars


def write_entry(path, text):
    """Write text to path, creating parent dirs; deterministic UTF-8, no newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    try:
        chars = validate(FORTUNE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    write_entry(path, FORTUNE)
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
