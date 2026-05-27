"""CLI entry point: `python -m new_lesson NN-name`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from new_lesson.scaffold import scaffold


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="new_lesson",
        description="Scaffold a new python-training lesson",
    )
    parser.add_argument("name", help="lesson slug, e.g. 01-hello")
    parser.add_argument(
        "--lessons-dir",
        type=Path,
        default=Path("lessons"),
        help="directory where the lesson is created (default: ./lessons)",
    )
    args = parser.parse_args(argv)

    try:
        target = scaffold(args.name, args.lessons_dir)
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"created {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
