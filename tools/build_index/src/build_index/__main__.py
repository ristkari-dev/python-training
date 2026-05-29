"""CLI: `python -m build_index --lessons lessons --shared shared/reveal --out dist`."""

from __future__ import annotations

import argparse
from pathlib import Path

from build_index.builder import build


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="build_index",
        description="Build the static slides site into an output directory",
    )
    parser.add_argument("--lessons", type=Path, default=Path("lessons"))
    parser.add_argument("--shared", type=Path, default=Path("shared/reveal"))
    parser.add_argument("--out", type=Path, default=Path("dist"))
    args = parser.parse_args(argv)

    build(args.lessons, args.shared, args.out)
    print(f"built {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
