"""HTTP handler factory for serving a single lesson's reveal.js deck."""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from mimetypes import guess_type
from pathlib import Path


def resolve_lesson(repo_root: Path, lesson: str) -> Path:
    """Return the lesson directory or raise FileNotFoundError."""
    lesson_dir = repo_root / "lessons" / lesson
    slides_dir = lesson_dir / "slides"
    if not slides_dir.is_dir():
        raise FileNotFoundError(
            f"no slides for lesson {lesson!r} (expected {slides_dir})"
        )
    return lesson_dir


def build_handler(
    repo_root: Path, lesson: str
) -> type[BaseHTTPRequestHandler]:
    """Return a handler class wired to serve one lesson + shared assets."""
    lesson_dir = resolve_lesson(repo_root, lesson)
    slides_root = lesson_dir / "slides"
    shared_root = repo_root / "shared" / "reveal"

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler API)
            path = self.path.split("?", 1)[0].lstrip("/")
            target = _resolve(path, slides_root, shared_root)
            if target is None:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            data = target.read_bytes()
            content_type = guess_type(target.name)[0] or "application/octet-stream"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format: str, *args: object) -> None:
            # Quiet by default; tests don't need the access log.
            return

    return Handler


def _resolve(path: str, slides_root: Path, shared_root: Path) -> Path | None:
    if path in ("", "index.html"):
        candidate = slides_root / "index.html"
        return candidate if candidate.is_file() else None
    if path.startswith("shared/reveal/"):
        candidate = shared_root / path[len("shared/reveal/"):]
    else:
        candidate = slides_root / path
    candidate = candidate.resolve()
    base = (
        shared_root.resolve()
        if path.startswith("shared/reveal/")
        else slides_root.resolve()
    )
    # Path traversal guard: candidate must stay under its base.
    try:
        candidate.relative_to(base)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None
