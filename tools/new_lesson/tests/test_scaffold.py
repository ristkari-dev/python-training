from pathlib import Path

import pytest
from new_lesson.scaffold import parse_name, scaffold


class TestParseName:
    def test_valid_two_digit_name(self) -> None:
        assert parse_name("01-hello") == ("01-hello", "01", "Hello")

    def test_multi_word_kebab(self) -> None:
        assert parse_name("17-select-timers") == (
            "17-select-timers",
            "17",
            "Select Timers",
        )

    @pytest.mark.parametrize(
        "raw",
        [
            "1-hello",            # number must be two digits
            "001-hello",          # number must be two digits
            "01_hello",           # underscore, not kebab
            "01-Hello",           # uppercase in slug
            "hello",              # no number
            "01-",                # empty slug
            "",                   # empty
            "01-hello/extra",     # slash not allowed
        ],
    )
    def test_rejects_invalid_names(self, raw: str) -> None:
        with pytest.raises(ValueError):
            parse_name(raw)


class TestScaffold:
    def test_creates_lesson_directory(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        result = scaffold("99-demo", lessons)
        assert result == lessons / "99-demo"
        assert result.is_dir()

    def test_renders_template_files(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        lesson_dir = scaffold("99-demo", lessons)
        readme = (lesson_dir / "README.md").read_text()
        assert "Lesson 99" in readme
        assert "Demo" in readme
        # template suffix is stripped
        assert not (lesson_dir / "README.md.tmpl").exists()

    def test_renders_index_html_with_title(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        lesson_dir = scaffold("99-demo", lessons)
        index = (lesson_dir / "slides" / "index.html").read_text()
        assert "<title>Lesson 99 — Demo</title>" in index

    def test_renders_exercises_and_solutions(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        lesson_dir = scaffold("99-demo", lessons)
        ex = (lesson_dir / "exercises" / "main.py").read_text()
        sol = (lesson_dir / "solutions" / "main.py").read_text()
        assert "lesson 99" in ex
        assert "hello from lesson 99" in sol

    def test_preserves_non_template_files(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        lesson_dir = scaffold("99-demo", lessons)
        # __init__.py files are copied as-is (no .tmpl suffix to strip)
        assert (lesson_dir / "exercises" / "__init__.py").exists()
        assert (lesson_dir / "solutions" / "__init__.py").exists()
        assert (lesson_dir / "slides" / "assets" / ".gitkeep").exists()

    def test_refuses_to_overwrite(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        scaffold("99-demo", lessons)
        with pytest.raises(FileExistsError):
            scaffold("99-demo", lessons)
