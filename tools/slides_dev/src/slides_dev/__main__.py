"""CLI entry point: `python -m slides_dev --lesson NN-name`."""

from __future__ import annotations

import argparse
import sys
from http.server import HTTPServer
from pathlib import Path

from slides_dev.server import build_handler


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="slides_dev",
        description="Serve one lesson's reveal.js deck locally",
    )
    parser.add_argument("--lesson", required=True, help="lesson slug, e.g. 01-hello")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="path to the python-training repo root (default: cwd)",
    )
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args(argv)

    try:
        handler = build_handler(args.repo_root, args.lesson)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    server = HTTPServer((args.host, args.port), handler)
    print(
        f"serving lesson {args.lesson} on http://{args.host}:{args.port} "
        f"(Ctrl-C to stop)"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
