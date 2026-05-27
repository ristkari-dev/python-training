from __future__ import annotations

import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from http.server import HTTPServer
from pathlib import Path

import pytest
from slides_dev.server import build_handler, resolve_lesson


def _make_repo(tmp_path: Path) -> Path:
    """Build a minimal repo skeleton: one lesson + shared/reveal."""
    lesson_slides = tmp_path / "lessons" / "01-hello" / "slides"
    lesson_slides.mkdir(parents=True)
    (lesson_slides / "index.html").write_text("<html>hello deck</html>")
    (lesson_slides / "slides.md").write_text("# slides")

    reveal = tmp_path / "shared" / "reveal" / "dist"
    reveal.mkdir(parents=True)
    (reveal / "reveal.css").write_text("/* reveal */")
    return tmp_path


class TestResolveLesson:
    def test_returns_path_when_slides_exist(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        assert resolve_lesson(repo, "01-hello") == repo / "lessons" / "01-hello"

    def test_raises_when_lesson_missing(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        with pytest.raises(FileNotFoundError):
            resolve_lesson(repo, "99-missing")

    def test_raises_when_slides_dir_missing(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        (repo / "lessons" / "02-no-slides").mkdir(parents=True)
        with pytest.raises(FileNotFoundError):
            resolve_lesson(repo, "02-no-slides")


@pytest.fixture
def running_server(tmp_path: Path) -> Iterator[tuple[str, HTTPServer]]:
    repo = _make_repo(tmp_path)
    handler = build_handler(repo, "01-hello")
    server = HTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}", server
    finally:
        server.shutdown()
        server.server_close()


class TestHandler:
    def test_root_serves_lesson_index(
        self, running_server: tuple[str, HTTPServer]
    ) -> None:
        url, _ = running_server
        with urllib.request.urlopen(f"{url}/") as resp:
            assert resp.status == 200
            assert b"hello deck" in resp.read()

    def test_slides_md_served(
        self, running_server: tuple[str, HTTPServer]
    ) -> None:
        url, _ = running_server
        with urllib.request.urlopen(f"{url}/slides.md") as resp:
            assert resp.status == 200
            assert b"# slides" in resp.read()

    def test_shared_reveal_served(
        self, running_server: tuple[str, HTTPServer]
    ) -> None:
        url, _ = running_server
        with urllib.request.urlopen(
            f"{url}/shared/reveal/dist/reveal.css"
        ) as resp:
            assert resp.status == 200
            assert b"/* reveal */" in resp.read()

    def test_unknown_path_404(
        self, running_server: tuple[str, HTTPServer]
    ) -> None:
        url, _ = running_server
        with pytest.raises(urllib.error.HTTPError) as exc:
            urllib.request.urlopen(f"{url}/nope.txt")
        assert exc.value.code == 404
