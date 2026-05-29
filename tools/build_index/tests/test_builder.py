from pathlib import Path

from build_index.builder import (
    build,
    collect_published,
    copy_tree,
    escape_html,
    render_index,
)


def test_escape_html_escapes_special_chars() -> None:
    assert escape_html("a & b < c > d") == "a &amp; b &lt; c &gt; d"


class TestCollectPublished:
    def test_finds_lessons_with_slides_subdir(self, tmp_path: Path) -> None:
        (tmp_path / "01-hello" / "slides").mkdir(parents=True)
        (tmp_path / "02-variables").mkdir(parents=True)  # no slides/
        published = collect_published(tmp_path)
        assert published == {"01-hello"}

    def test_empty_when_dir_missing(self, tmp_path: Path) -> None:
        assert collect_published(tmp_path / "nonexistent") == set()

    def test_ignores_files_at_top_level(self, tmp_path: Path) -> None:
        (tmp_path / "01-hello" / "slides").mkdir(parents=True)
        (tmp_path / "stray.txt").write_text("x")
        assert collect_published(tmp_path) == {"01-hello"}


class TestCopyTree:
    def test_copies_files_and_dirs(self, tmp_path: Path) -> None:
        src = tmp_path / "src"
        (src / "sub").mkdir(parents=True)
        (src / "a.txt").write_text("a")
        (src / "sub" / "b.txt").write_text("b")
        dst = tmp_path / "dst"
        copy_tree(src, dst)
        assert (dst / "a.txt").read_text() == "a"
        assert (dst / "sub" / "b.txt").read_text() == "b"

    def test_noop_when_src_missing(self, tmp_path: Path) -> None:
        dst = tmp_path / "dst"
        copy_tree(tmp_path / "nope", dst)
        assert not dst.exists()


class TestRenderIndex:
    def test_published_lesson_is_a_link(self) -> None:
        html = render_index({"01-hello"})
        assert '<a class="lesson" href="lessons/01-hello/slides/">' in html

    def test_unpublished_lesson_is_future_placeholder(self) -> None:
        html = render_index(set())
        assert '<div class="lesson future" aria-disabled="true">' in html

    def test_contains_title_and_phase_headers(self) -> None:
        html = render_index(set())
        assert "<title>Python Training</title>" in html
        assert "Phase 1 · Foundations" in html
        assert "Phase 4 · Production &amp; Services" in html

    def test_lesson_titles_present(self) -> None:
        html = render_index(set())
        assert "Hello, Python" in html
        assert "Distributed patterns &amp; wrap-up" in html

    def test_published_lesson_not_also_future(self) -> None:
        html = render_index({"01-hello"})
        assert html.count('class="lesson future"') == 27


class TestBuild:
    def test_produces_index_and_copies(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        (lessons / "01-hello" / "slides").mkdir(parents=True)
        (lessons / "01-hello" / "slides" / "index.html").write_text("deck")
        shared = tmp_path / "shared" / "reveal" / "dist"
        shared.mkdir(parents=True)
        (shared / "reveal.css").write_text("/* css */")
        out = tmp_path / "dist"

        build(lessons, tmp_path / "shared" / "reveal", out)

        assert (out / "index.html").exists()
        assert (out / "lessons" / "01-hello" / "slides" / "index.html").read_text() == "deck"
        assert (out / "shared" / "reveal" / "dist" / "reveal.css").read_text() == "/* css */"
        index = (out / "index.html").read_text()
        assert "<title>Python Training</title>" in index
        assert '<a class="lesson" href="lessons/01-hello/slides/">' in index

    def test_overwrites_stale_out_dir(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        (lessons / "01-hello" / "slides").mkdir(parents=True)
        out = tmp_path / "dist"
        out.mkdir()
        (out / "stale.txt").write_text("stale")

        build(lessons, tmp_path / "shared" / "reveal", out)

        assert not (out / "stale.txt").exists()
        assert (out / "index.html").exists()

    def test_handles_zero_published_lessons(self, tmp_path: Path) -> None:
        # Mirrors the current repo state: no lessons authored yet.
        out = tmp_path / "dist"
        build(tmp_path / "lessons", tmp_path / "shared" / "reveal", out)
        index = (out / "index.html").read_text()
        assert "<title>Python Training</title>" in index
        # All 28 lessons render as future placeholders.
        assert index.count('class="lesson future"') == 28
