# Plan A — Foundation Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap the `python-training` repo with a working uv workspace, ruff/mypy/pytest configuration, vendored reveal.js, custom theme, lesson scaffolder, local slides dev server, Makefile, and contributor docs — so that `make new-lesson NAME=99-demo` produces a working lesson and `make slides-dev LESSON=99-demo` serves it locally.

**Architecture:** Single uv workspace at the root with members declared under `lessons/*` and `tools/*`. Two small Python programs under `tools/`: `new_lesson` (generates a lesson folder from an on-disk template) and `slides_dev` (stdlib `http.server`-based static server that mounts the lesson's `slides/` plus the shared `reveal/` assets). Reveal.js 5.1.0 is vendored under `shared/reveal/` and shared across all decks. A single Makefile is the canonical entry point for every workflow. No npm, no Node — Python stdlib + vendored static assets only.

**Tech Stack:** Python 3.13, `uv` (latest), `ruff`, `mypy`, `pytest`, reveal.js 5.1.0 (vendored), GNU Make.

---

## File Structure

After this plan completes, the repo contains:

```
python-training/
├── README.md                                 (already exists; refreshed in Task 12)
├── CONTRIBUTING.md                           (Task 12)
├── pyproject.toml                            (Task 1; root workspace + tool config)
├── uv.lock                                   (Task 1; committed)
├── Makefile                                  (Task 11)
├── .gitignore                                (already exists)
├── .editorconfig                             (Task 1)
├── .python-version                           (Task 1)
│
├── shared/
│   └── reveal/                               (Task 2)
│       ├── LICENSE
│       ├── VERSION
│       ├── dist/                             (vendored reveal.js distributables)
│       ├── plugin/                           (vendored reveal.js plugins)
│       └── theme/
│           └── python-training.css           (Task 3)
│
├── tools/
│   ├── new_lesson/
│   │   ├── pyproject.toml                    (Task 4)
│   │   ├── src/
│   │   │   └── new_lesson/
│   │   │       ├── __init__.py               (Task 4)
│   │   │       ├── __main__.py               (Task 6)
│   │   │       └── scaffold.py               (Task 5)
│   │   ├── tests/
│   │   │   ├── __init__.py                   (Task 5)
│   │   │   └── test_scaffold.py              (Task 5)
│   │   └── template/                         (Task 4)
│   │       ├── pyproject.toml.tmpl
│   │       ├── README.md.tmpl
│   │       ├── slides/
│   │       │   ├── index.html.tmpl
│   │       │   ├── slides.md.tmpl
│   │       │   └── assets/
│   │       │       └── .gitkeep
│   │       ├── exercises/
│   │       │   ├── __init__.py
│   │       │   ├── main.py.tmpl
│   │       │   └── test_main.py.tmpl
│   │       └── solutions/
│   │           ├── __init__.py
│   │           ├── main.py.tmpl
│   │           └── test_main.py.tmpl
│   └── slides_dev/
│       ├── pyproject.toml                    (Task 8)
│       ├── src/
│       │   └── slides_dev/
│       │       ├── __init__.py               (Task 8)
│       │       ├── __main__.py               (Task 10)
│       │       └── server.py                 (Task 9)
│       └── tests/
│           ├── __init__.py                   (Task 9)
│           └── test_server.py                (Task 9)
│
└── docs/
    └── superpowers/
        ├── specs/                            (already exists)
        └── plans/                            (already exists)
```

### Decomposition rationale

- `new_lesson` is split into single-responsibility units inside one package: `parse_name` (input validation), `scaffold` (filesystem + template rendering), and `__main__` (CLI wiring + sys.exit). Each is testable in isolation; the package stays small enough to read in one screen.
- `slides_dev` keeps `build_handler` (factory function) separate from `__main__` so the handler is unit-testable without binding a real socket.
- Each tool is a uv workspace member with a `src/` layout — `uv sync` makes them importable as `new_lesson` and `slides_dev` from the workspace venv.
- The lesson template lives under `tools/new_lesson/template/` and is resolved at runtime via `importlib.resources.files("new_lesson") / "../../template"`. The template directory is included via `[tool.hatch.build.targets.wheel.force-include]`. Plain-text templates use stdlib `string.Template` substitution; no jinja2 dependency.

### Why the `src/` layout for tools

Workspace members built into the shared venv must be importable. The `src/` layout keeps the import path (`new_lesson`) decoupled from the working directory and prevents accidental "works because of cwd" bugs.

---

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command. Do not `cd` elsewhere unless explicitly told.
- **Commit messages:** Conventional Commits (`feat:`, `chore:`, `docs:`, `test:`, `build:`).
- **Python version:** 3.13. If a different version is required, change `.python-version` in Task 1 before continuing — it cascades to CI (Plan B) and Dockerfile (Plan B).
- **Reveal.js version:** 5.1.0 — pinned. Already vendored in the sibling `go-training` repo at `/Users/ristkari/code/private/go-training/shared/reveal/`; copying from there is the recommended path in Task 2.
- **Repo state at start of plan:** One commit (`a099f36`) with `README.md`, `.gitignore`, and the design spec. Remote `origin` points at `git@github.com:ristkari-dev/python-training.git`. Branch `main` tracks `origin/main`.
- **Dependency management:** Use `uv add`, `uv remove`, and `uv sync`. Do not hand-edit `[project.dependencies]` blocks in `pyproject.toml`. (Hand-edits to `[tool.*]` config blocks are fine.)

---

## Task 1: Initialize uv workspace and base config files

**Files:**
- Create: `pyproject.toml`
- Create: `uv.lock`
- Create: `.editorconfig`
- Create: `.python-version`

- [ ] **Step 1: Create `.python-version`**

```
3.13
```

- [ ] **Step 2: Create `.editorconfig`**

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{md,html,css,yml,yaml,toml}]
indent_size = 2

[Makefile]
indent_style = tab
```

- [ ] **Step 3: Create root `pyproject.toml`**

```toml
[project]
name = "python-training"
version = "0.0.0"
description = "A Python programming course delivered as code + per-lesson reveal.js slide decks"
requires-python = ">=3.13"

[tool.uv.workspace]
members = ["lessons/*", "tools/*"]

[tool.uv]
package = false

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "B", "SIM", "TID"]

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.13"
strict = true
exclude = ["lessons/", ".venv/", "build/", "dist/"]

[tool.pytest.ini_options]
testpaths = ["tools", "lessons"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

> **Why `package = false`:** the root project is not installable; it's only a workspace coordinator. Tools and lessons declare their own `[project]` blocks.

> **Why mypy `exclude` instead of per-module overrides:** lesson directories use kebab-case names like `01-hello/` that aren't valid Python module identifiers, so `[[tool.mypy.overrides]] module = ["lessons.*"]` wouldn't match. The Phase 2 plan (lesson 9 onward) will widen `make typecheck` by adding explicit paths like `lessons/09-types/solutions`, opting those lessons into strict checking by listing them in the Make target rather than via mypy module patterns.

- [ ] **Step 4: Install Python 3.13 via uv and create the venv**

Run: `uv python install 3.13`
Then: `uv sync`

Expected: uv prints "Using CPython 3.13.x" and creates `.venv/` plus `uv.lock`.

- [ ] **Step 5: Sanity-check the venv**

Run: `uv run python --version`
Expected: `Python 3.13.x`

Run: `uv run python -c "import sys; print(sys.executable)"`
Expected: a path inside `.venv/`.

- [ ] **Step 6: Add dev tools (ruff, mypy, pytest) as workspace dev dependencies**

Run: `uv add --dev ruff mypy pytest`

Expected: `pyproject.toml` gains a `[dependency-groups]` section with `dev = ["ruff>=...", "mypy>=...", "pytest>=..."]`, and `uv.lock` is updated.

- [ ] **Step 7: Verify each tool runs**

Run: `uv run ruff --version`
Expected: prints a ruff version string.

Run: `uv run mypy --version`
Expected: prints `mypy 1.x.x ...`.

Run: `uv run pytest --version`
Expected: prints `pytest 8.x.x` or similar.

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml uv.lock .editorconfig .python-version
git commit -m "chore: initialize uv workspace, pin Python 3.13, configure ruff/mypy/pytest"
```

---

## Task 2: Vendor reveal.js 5.1.0

**Files:**
- Create: `shared/reveal/dist/...`
- Create: `shared/reveal/plugin/...`
- Create: `shared/reveal/LICENSE`
- Create: `shared/reveal/VERSION`

The sibling `go-training` repo at `/Users/ristkari/code/private/go-training/shared/reveal/` already contains the vendored reveal.js 5.1.0 tree. Copy from there.

- [ ] **Step 1: Verify the source exists**

Run: `ls /Users/ristkari/code/private/go-training/shared/reveal/`
Expected: lists `LICENSE`, `VERSION`, `dist`, `plugin`, `theme`, `fonts`.

Run: `cat /Users/ristkari/code/private/go-training/shared/reveal/VERSION`
Expected: starts with `reveal.js 5.1.0`.

- [ ] **Step 2: Copy `dist/`, `plugin/`, `LICENSE` into `shared/reveal/`**

Run:
```bash
mkdir -p shared/reveal
cp -R /Users/ristkari/code/private/go-training/shared/reveal/dist shared/reveal/
cp -R /Users/ristkari/code/private/go-training/shared/reveal/plugin shared/reveal/
cp /Users/ristkari/code/private/go-training/shared/reveal/LICENSE shared/reveal/LICENSE
```

> **Do not copy `theme/` or `fonts/`** — `theme/` is go-training-specific; we ship our own theme in Task 3. The `fonts/` tree in go-training is for that theme; the python-training theme will be font-free in Plan A (theme polish is deferred).

- [ ] **Step 3: Write `shared/reveal/VERSION`**

```
reveal.js 5.1.0
Source: https://github.com/hakimel/reveal.js/releases/tag/5.1.0
Vendored: 2026-05-25
Upgrade: re-download the tarball, replace dist/ and plugin/, update this file.
```

- [ ] **Step 4: Spot-check key files**

Run: `ls shared/reveal/dist/`
Expected: includes `reveal.css`, `reveal.js`, `reset.css`, `theme/`.

Run: `ls shared/reveal/plugin/`
Expected: includes `markdown`, `highlight`, `notes`, `search`.

- [ ] **Step 5: Commit**

```bash
git add shared/reveal/
git commit -m "build: vendor reveal.js 5.1.0 under shared/reveal/"
```

---

## Task 3: Add custom slide theme

**Files:**
- Create: `shared/reveal/theme/python-training.css`

Minimal functional theme: imports reveal.js's `black` base, overrides accent color (Python yellow `#FFD43B` on Python blue `#3776AB`), enlarges code blocks. Theme polish is intentionally deferred to a later plan (mirrors the go-training "theming overhaul" arc).

- [ ] **Step 1: Create `shared/reveal/theme/python-training.css`**

```css
/*
 * python-training reveal.js theme — Python-branded dark
 *
 * Minimal baseline: imports the upstream `black` theme and overrides the
 * accent palette + code-block typography for readability during live coding.
 * Theme polish (custom fonts, slide patterns, code highlighting) is deferred
 * to a separate "theming overhaul" plan.
 */

@import url("../dist/theme/black.css");

:root {
  --python-blue: #3776AB;
  --python-yellow: #FFD43B;
}

.reveal {
  --r-link-color: var(--python-yellow);
  --r-link-color-hover: #FFFFFF;
  --r-selection-background-color: var(--python-yellow);
  --r-selection-color: #1A1A1A;
  --r-heading-color: #FFFFFF;
}

.reveal h1,
.reveal h2,
.reveal h3 {
  text-transform: none;
  letter-spacing: -0.01em;
}

.reveal pre {
  font-size: 0.7em;
  line-height: 1.4;
  box-shadow: none;
  border-left: 4px solid var(--python-yellow);
}

.reveal pre code {
  padding: 1em 1.2em;
  max-height: 600px;
}

.reveal code {
  background: rgba(255, 212, 59, 0.08);
  border-radius: 3px;
  padding: 0.1em 0.3em;
}
```

- [ ] **Step 2: Verify the file is valid CSS**

Run: `python3 -c "open('shared/reveal/theme/python-training.css').read(); print('ok')"`
Expected: `ok`.

(No browser-level verification in this task — that happens at the end-to-end smoke test in Task 7.)

- [ ] **Step 3: Commit**

```bash
git add shared/reveal/theme/python-training.css
git commit -m "feat(theme): add minimal python-training reveal.js theme"
```

---

## Task 4: Create the `new_lesson` tool skeleton and template tree

**Files:**
- Create: `tools/new_lesson/pyproject.toml`
- Create: `tools/new_lesson/src/new_lesson/__init__.py`
- Create: `tools/new_lesson/template/pyproject.toml.tmpl`
- Create: `tools/new_lesson/template/README.md.tmpl`
- Create: `tools/new_lesson/template/slides/index.html.tmpl`
- Create: `tools/new_lesson/template/slides/slides.md.tmpl`
- Create: `tools/new_lesson/template/slides/assets/.gitkeep`
- Create: `tools/new_lesson/template/exercises/__init__.py`
- Create: `tools/new_lesson/template/exercises/main.py.tmpl`
- Create: `tools/new_lesson/template/exercises/test_main.py.tmpl`
- Create: `tools/new_lesson/template/solutions/__init__.py`
- Create: `tools/new_lesson/template/solutions/main.py.tmpl`
- Create: `tools/new_lesson/template/solutions/test_main.py.tmpl`

- [ ] **Step 1: Create `tools/new_lesson/pyproject.toml`**

```toml
[project]
name = "new-lesson"
version = "0.0.0"
description = "Scaffold a new python-training lesson from the template tree"
requires-python = ">=3.13"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/new_lesson"]

[tool.hatch.build.targets.wheel.force-include]
"template" = "new_lesson/template"
```

> **Why `force-include`:** the template directory lives next to `src/`, not inside the package. `force-include` ships it inside the installed package so `importlib.resources.files("new_lesson") / "template"` resolves correctly.

- [ ] **Step 2: Create `tools/new_lesson/src/new_lesson/__init__.py`**

```python
"""Scaffold a new python-training lesson from the template tree."""
```

- [ ] **Step 3: Create `tools/new_lesson/template/pyproject.toml.tmpl`**

```toml
[project]
name = "lesson-${name}"
version = "0.0.0"
description = "Lesson ${number}: ${title}"
requires-python = ">=3.13"

[tool.uv]
package = false
```

- [ ] **Step 4: Create `tools/new_lesson/template/README.md.tmpl`**

````markdown
# Lesson ${number} — ${title}

## Learning goals

- TODO: 3-5 bullets.

## Prereqs

- TODO: links to earlier lessons.

## Concepts

TODO: 1-3 paragraphs mirroring the deck narrative for self-study.

## Exercise brief

TODO: what students build; what `pytest` should show when done.

## How to run

```bash
uv run pytest lessons/${name}/exercises
```

## Going further

- TODO: optional advanced material.
````

- [ ] **Step 5: Create `tools/new_lesson/template/slides/index.html.tmpl`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <title>Lesson ${number} — ${title}</title>
  <link rel="stylesheet" href="../../shared/reveal/dist/reveal.css">
  <link rel="stylesheet" href="../../shared/reveal/theme/python-training.css">
  <link rel="stylesheet" href="../../shared/reveal/plugin/highlight/monokai.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section data-markdown="slides.md"
               data-separator="^---$"
               data-separator-vertical="^--$"
               data-separator-notes="^Note:"></section>
    </div>
  </div>
  <script type="module">
    import Reveal from "../../shared/reveal/dist/reveal.esm.js";
    import Markdown from "../../shared/reveal/plugin/markdown/markdown.esm.js";
    import Highlight from "../../shared/reveal/plugin/highlight/highlight.esm.js";
    import Notes from "../../shared/reveal/plugin/notes/notes.esm.js";
    import Search from "../../shared/reveal/plugin/search/search.esm.js";
    Reveal.initialize({
      hash: true,
      plugins: [Markdown, Highlight, Notes, Search]
    });
  </script>
</body>
</html>
```

- [ ] **Step 6: Create `tools/new_lesson/template/slides/slides.md.tmpl`**

```markdown
## Lesson ${number}
### ${title}

One-line learning goal goes here.

Note:
Speaker notes go here.

---

## What's next

A pointer to the next lesson.
```

- [ ] **Step 7: Create `tools/new_lesson/template/slides/assets/.gitkeep`**

(Empty file. Used so git tracks the otherwise-empty assets directory.)

- [ ] **Step 8: Create `tools/new_lesson/template/exercises/__init__.py`**

```python
```

(Empty.)

- [ ] **Step 9: Create `tools/new_lesson/template/exercises/main.py.tmpl`**

```python
def hello() -> str:
    raise NotImplementedError("lesson ${number} exercise")
```

- [ ] **Step 10: Create `tools/new_lesson/template/exercises/test_main.py.tmpl`**

```python
from exercises.main import hello


def test_hello_returns_greeting() -> None:
    assert hello() == "hello from lesson ${number}"
```

- [ ] **Step 11: Create `tools/new_lesson/template/solutions/__init__.py`**

```python
```

(Empty.)

- [ ] **Step 12: Create `tools/new_lesson/template/solutions/main.py.tmpl`**

```python
def hello() -> str:
    return "hello from lesson ${number}"
```

- [ ] **Step 13: Create `tools/new_lesson/template/solutions/test_main.py.tmpl`**

```python
from solutions.main import hello


def test_hello_returns_greeting() -> None:
    assert hello() == "hello from lesson ${number}"
```

- [ ] **Step 14: Sync the workspace to register the new member**

Run: `uv sync`
Expected: uv prints "Audited X packages" or similar; no errors. The `new-lesson` package is now installed in the workspace venv.

- [ ] **Step 15: Verify the package imports**

Run: `uv run python -c "import new_lesson; from importlib.resources import files; print((files('new_lesson') / 'template').is_dir())"`
Expected: `True`.

- [ ] **Step 16: Commit**

```bash
git add tools/new_lesson/pyproject.toml tools/new_lesson/src tools/new_lesson/template uv.lock
git commit -m "feat(tools): add new_lesson package skeleton and template tree"
```

---

## Task 5: Implement `new_lesson.scaffold` with tests

**Files:**
- Create: `tools/new_lesson/src/new_lesson/scaffold.py`
- Create: `tools/new_lesson/tests/__init__.py`
- Create: `tools/new_lesson/tests/test_scaffold.py`

Two responsibilities, each with its own function:
- `parse_name(raw: str) -> tuple[str, str, str]` — validates and splits `"NN-kebab-name"` into `(name, number, title)`. Title is derived by replacing dashes with spaces and title-casing the part after the number.
- `scaffold(name: str, lessons_dir: Path) -> Path` — copies the template tree into `lessons_dir / name`, substitutes `${name}`, `${number}`, `${title}` in `.tmpl` files (and strips the `.tmpl` suffix), refuses to overwrite an existing folder.

- [ ] **Step 1: Create the tests package init**

Path: `tools/new_lesson/tests/__init__.py`

```python
```

(Empty.)

- [ ] **Step 2: Write the failing tests**

Path: `tools/new_lesson/tests/test_scaffold.py`

```python
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
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `uv run pytest tools/new_lesson/tests -v`
Expected: collection error or all tests fail with `ImportError: cannot import name 'parse_name' from 'new_lesson.scaffold'`.

- [ ] **Step 4: Implement `scaffold.py`**

Path: `tools/new_lesson/src/new_lesson/scaffold.py`

```python
"""Scaffold a new lesson directory from the template tree."""

from __future__ import annotations

import re
import shutil
from importlib.resources import as_file, files
from pathlib import Path
from string import Template

_NAME_RE = re.compile(r"^(\d{2})-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$")


def parse_name(raw: str) -> tuple[str, str, str]:
    """Validate a lesson slug and derive its number + title.

    Returns: (name, number, title). Title is derived by replacing dashes
    with spaces and title-casing each word.
    """
    match = _NAME_RE.match(raw)
    if not match:
        raise ValueError(
            f"invalid lesson name {raw!r}: expected 'NN-kebab-name' "
            f"(e.g., '01-hello', '17-select-timers')"
        )
    number, slug = match.group(1), match.group(2)
    title = " ".join(word.capitalize() for word in slug.split("-"))
    return raw, number, title


def scaffold(name: str, lessons_dir: Path) -> Path:
    """Copy the template tree to lessons_dir/name with substitutions.

    Returns the path to the created lesson directory. Refuses to overwrite
    an existing directory; raises FileExistsError if one is present.
    """
    parsed_name, number, title = parse_name(name)
    target = lessons_dir / parsed_name
    if target.exists():
        raise FileExistsError(f"lesson already exists: {target}")

    substitutions = {"name": parsed_name, "number": number, "title": title}
    template_anchor = files("new_lesson") / "template"
    with as_file(template_anchor) as template_dir:
        _copy_with_substitution(template_dir, target, substitutions)
    return target


def _copy_with_substitution(
    source: Path, target: Path, substitutions: dict[str, str]
) -> None:
    target.mkdir(parents=True, exist_ok=False)
    for entry in source.iterdir():
        if entry.is_dir():
            _copy_with_substitution(entry, target / entry.name, substitutions)
            continue
        if entry.suffix == ".tmpl":
            rendered = Template(entry.read_text()).substitute(substitutions)
            (target / entry.stem).write_text(rendered)
        else:
            shutil.copy2(entry, target / entry.name)
```

> **Why `Template.substitute` over `.safe_substitute`:** `substitute` raises if a template references an unknown variable. We want loud failures, not silent omissions.

- [ ] **Step 5: Run the tests to verify they pass**

Run: `uv run pytest tools/new_lesson/tests -v`
Expected: all tests pass.

- [ ] **Step 6: Run ruff + mypy on the new code**

Run: `uv run ruff check tools/new_lesson`
Expected: no issues.

Run: `uv run mypy tools/new_lesson/src`
Expected: `Success: no issues found in N source files`.

- [ ] **Step 7: Commit**

```bash
git add tools/new_lesson/src/new_lesson/scaffold.py tools/new_lesson/tests
git commit -m "feat(new_lesson): implement parse_name and scaffold with tests"
```

---

## Task 6: Wire up the `new_lesson` CLI

**Files:**
- Create: `tools/new_lesson/src/new_lesson/__main__.py`

- [ ] **Step 1: Write the CLI**

Path: `tools/new_lesson/src/new_lesson/__main__.py`

```python
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
```

- [ ] **Step 2: Smoke-test the CLI with `--help`**

Run: `uv run python -m new_lesson --help`
Expected: argparse prints usage block including `name` positional and `--lessons-dir`.

- [ ] **Step 3: Smoke-test with a sandbox lesson**

Run: `uv run python -m new_lesson 99-demo`
Expected: prints `created lessons/99-demo`; directory `lessons/99-demo` exists with the expected files.

- [ ] **Step 4: Smoke-test the rejection path**

Run: `uv run python -m new_lesson 99-demo`
Expected: prints `error: lesson already exists: lessons/99-demo` to stderr; exit code 1.

Run: `uv run python -m new_lesson bad_name`
Expected: prints an error about invalid name; exit code 1.

- [ ] **Step 5: Verify the generated lesson's tests run and behave as designed**

Run: `uv run pytest lessons/99-demo/exercises`
Expected: 1 test FAILS with `NotImplementedError` (the spec for the student).

Run: `uv run pytest lessons/99-demo/solutions`
Expected: 1 test passes.

- [ ] **Step 6: Clean up the sandbox**

```bash
rm -rf lessons/99-demo
```

- [ ] **Step 7: Lint and type-check**

Run: `uv run ruff check tools/new_lesson`
Expected: no issues.

Run: `uv run mypy tools/new_lesson/src`
Expected: `Success`.

- [ ] **Step 8: Commit**

```bash
git add tools/new_lesson/src/new_lesson/__main__.py
git commit -m "feat(new_lesson): add CLI entry point"
```

---

## Task 7: Add an end-to-end test for `new_lesson`

**Files:**
- Modify: `tools/new_lesson/tests/test_scaffold.py` (append new test class)

The unit tests in Task 5 use the template tree directly. This task adds one end-to-end test that runs the CLI as a subprocess to lock down the full path: argument parsing → scaffold → template resolution from the installed package.

- [ ] **Step 1: Append the end-to-end test**

In `tools/new_lesson/tests/test_scaffold.py`, append at the bottom:

```python
import subprocess
import sys


class TestCli:
    def test_creates_lesson_via_subprocess(self, tmp_path: Path) -> None:
        lessons = tmp_path / "lessons"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "new_lesson",
                "42-end-to-end",
                "--lessons-dir",
                str(lessons),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        assert "created" in result.stdout
        assert (lessons / "42-end-to-end" / "README.md").exists()

    def test_invalid_name_exits_nonzero(self, tmp_path: Path) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "new_lesson",
                "BAD",
                "--lessons-dir",
                str(tmp_path / "lessons"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "invalid lesson name" in result.stderr
```

> Adjust the new `import subprocess` and `import sys` lines so they sit with the other top-of-file imports.

- [ ] **Step 2: Run the new tests**

Run: `uv run pytest tools/new_lesson/tests -v`
Expected: all tests pass (including the two new ones).

- [ ] **Step 3: Commit**

```bash
git add tools/new_lesson/tests/test_scaffold.py
git commit -m "test(new_lesson): add end-to-end CLI tests"
```

---

## Task 8: Create the `slides_dev` tool skeleton

**Files:**
- Create: `tools/slides_dev/pyproject.toml`
- Create: `tools/slides_dev/src/slides_dev/__init__.py`

- [ ] **Step 1: Create `tools/slides_dev/pyproject.toml`**

```toml
[project]
name = "slides-dev"
version = "0.0.0"
description = "Local static server for a python-training lesson deck"
requires-python = ">=3.13"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/slides_dev"]
```

- [ ] **Step 2: Create `tools/slides_dev/src/slides_dev/__init__.py`**

```python
"""Local static server for serving a single lesson's reveal.js deck."""
```

- [ ] **Step 3: Sync the workspace**

Run: `uv sync`
Expected: uv installs `slides-dev` into the workspace venv.

- [ ] **Step 4: Verify import**

Run: `uv run python -c "import slides_dev; print(slides_dev.__doc__)"`
Expected: prints the docstring.

- [ ] **Step 5: Commit**

```bash
git add tools/slides_dev/pyproject.toml tools/slides_dev/src uv.lock
git commit -m "feat(tools): add slides_dev package skeleton"
```

---

## Task 9: Implement `slides_dev.server` with tests

**Files:**
- Create: `tools/slides_dev/src/slides_dev/server.py`
- Create: `tools/slides_dev/tests/__init__.py`
- Create: `tools/slides_dev/tests/test_server.py`

Design: a single factory `build_handler(repo_root: Path, lesson: str) -> type[BaseHTTPRequestHandler]` returns a handler class that serves:
- `/` and `/index.html` → the lesson's `slides/index.html` (so the deck loads at the root URL).
- `/slides/*` → files under `lessons/<lesson>/slides/`.
- `/shared/reveal/*` → files under `shared/reveal/`.
- Anything else → 404.

A `resolve_lesson(repo_root: Path, lesson: str) -> Path` helper validates the lesson exists. Both functions are pure (no network), so they're unit-tested with `unittest.mock` and `tempfile`. Two integration tests exercise the handler via `http.server`'s in-process testing approach: bind to port 0, issue requests with `urllib.request`, assert responses.

- [ ] **Step 1: Create the tests package init**

Path: `tools/slides_dev/tests/__init__.py`

```python
```

(Empty.)

- [ ] **Step 2: Write the failing tests**

Path: `tools/slides_dev/tests/test_server.py`

```python
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
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `uv run pytest tools/slides_dev/tests -v`
Expected: collection error or tests fail with `ImportError: cannot import name 'build_handler' from 'slides_dev.server'`.

- [ ] **Step 4: Implement `server.py`**

Path: `tools/slides_dev/src/slides_dev/server.py`

```python
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
```

> **Why the relative_to guard:** without it, a request for `..\\..\\etc\\passwd` could escape the served directory. `Path.resolve()` normalises the candidate, then `relative_to` enforces containment.

- [ ] **Step 5: Run the tests to verify they pass**

Run: `uv run pytest tools/slides_dev/tests -v`
Expected: all 7 tests pass.

- [ ] **Step 6: Lint and type-check**

Run: `uv run ruff check tools/slides_dev`
Expected: no issues.

Run: `uv run mypy tools/slides_dev/src`
Expected: `Success`.

- [ ] **Step 7: Commit**

```bash
git add tools/slides_dev/src/slides_dev/server.py tools/slides_dev/tests
git commit -m "feat(slides_dev): implement resolve_lesson and build_handler with tests"
```

---

## Task 10: Wire up the `slides_dev` CLI

**Files:**
- Create: `tools/slides_dev/src/slides_dev/__main__.py`

- [ ] **Step 1: Write the CLI**

Path: `tools/slides_dev/src/slides_dev/__main__.py`

```python
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
```

- [ ] **Step 2: Smoke-test with `--help`**

Run: `uv run python -m slides_dev --help`
Expected: argparse prints usage with `--lesson`, `--repo-root`, `--port`, `--host`.

- [ ] **Step 3: Smoke-test the error path**

Run: `uv run python -m slides_dev --lesson 99-nonexistent`
Expected: prints an error about missing slides to stderr; exit code 1.

- [ ] **Step 4: Lint and type-check**

Run: `uv run ruff check tools/slides_dev`
Expected: no issues.

Run: `uv run mypy tools/slides_dev/src`
Expected: `Success`.

- [ ] **Step 5: Commit**

```bash
git add tools/slides_dev/src/slides_dev/__main__.py
git commit -m "feat(slides_dev): add CLI entry point"
```

---

## Task 11: Write the Makefile

**Files:**
- Create: `Makefile`

- [ ] **Step 1: Write the Makefile**

```makefile
SHELL := /bin/bash
.DEFAULT_GOAL := help

REPO_ROOT := $(shell pwd)

.PHONY: help
help: ## List available targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: sync
sync: ## Install/refresh the workspace venv (uv sync)
	uv sync

.PHONY: test
test: ## Run solution tests (the ones that should always pass)
	@dirs=$$(find lessons -type d -name solutions 2>/dev/null); \
	if [ -z "$$dirs" ]; then echo "no solution directories yet"; else uv run pytest tools $$dirs; fi

.PHONY: test-exercises
test-exercises: ## Run exercise tests (these fail by design until students complete them)
	-@dirs=$$(find lessons -type d -name exercises 2>/dev/null); \
	if [ -z "$$dirs" ]; then echo "no exercise directories yet"; exit 0; fi; \
	uv run pytest $$dirs

.PHONY: test-lesson
test-lesson: ## Run tests for one lesson, both exercises and solutions (LESSON=NN-name)
	@test -n "$(LESSON)" || (echo "usage: make test-lesson LESSON=NN-name" && exit 1)
	-uv run pytest lessons/$(LESSON)/exercises
	uv run pytest lessons/$(LESSON)/solutions

.PHONY: lint
lint: ## Run ruff check
	uv run ruff check .

.PHONY: fmt
fmt: ## Format with ruff format + ruff check --fix
	uv run ruff format .
	uv run ruff check --fix .

.PHONY: typecheck
typecheck: ## Run mypy on tools and lesson solutions
	uv run mypy tools/new_lesson/src tools/slides_dev/src

.PHONY: new-lesson
new-lesson: ## Scaffold a new lesson (NAME=NN-name)
	@test -n "$(NAME)" || (echo "usage: make new-lesson NAME=NN-name" && exit 1)
	uv run python -m new_lesson $(NAME)

.PHONY: slides-dev
slides-dev: ## Serve one lesson's deck locally on http://localhost:8000 (LESSON=NN-name)
	@test -n "$(LESSON)" || (echo "usage: make slides-dev LESSON=NN-name" && exit 1)
	uv run python -m slides_dev --lesson $(LESSON) --repo-root $(REPO_ROOT)
```

> **Why `find` instead of glob in `test`:** `lessons/` may be empty during early development (it is, after Plan A). A bare `pytest lessons/*/solutions` would fail with "no such path". `find` returns nothing, which the shell skips.

> **`make typecheck` scope:** Plan A only ships `tools/`. Once lessons exist, lesson 9+ paths get added to this target (Phase 2 plan).

- [ ] **Step 2: Verify `make help` lists every target**

Run: `make help`
Expected: lists `help`, `sync`, `test`, `test-exercises`, `test-lesson`, `lint`, `fmt`, `typecheck`, `new-lesson`, `slides-dev`.

- [ ] **Step 3: Verify `make lint` is green**

Run: `make lint`
Expected: ruff reports no issues.

- [ ] **Step 4: Verify `make typecheck` is green**

Run: `make typecheck`
Expected: mypy reports `Success`.

- [ ] **Step 5: Verify `make test` runs the tool tests**

Run: `make test`
Expected: pytest collects and passes the tests under `tools/new_lesson/tests` and `tools/slides_dev/tests`. (`lessons/` is empty, so the find command prints "no solution directories yet" and exits.)

- [ ] **Step 6: Commit**

```bash
git add Makefile
git commit -m "build: add Makefile with sync/test/lint/fmt/new-lesson/slides-dev targets"
```

---

## Task 12: Write CONTRIBUTING.md and refresh README.md

**Files:**
- Create: `CONTRIBUTING.md`
- Modify: `README.md`

- [ ] **Step 1: Create `CONTRIBUTING.md`**

````markdown
# Contributing to python-training

## Adding a new lesson

```bash
make new-lesson NAME=NN-kebab-name      # e.g. 04-functions
make slides-dev LESSON=NN-kebab-name    # http://localhost:8000
make test-lesson LESSON=NN-kebab-name
```

The scaffolder enforces the `NN-kebab-name` format (two-digit number, lowercase kebab slug) and refuses to overwrite an existing folder.

## The four-file convention

Every lesson directory contains exactly four parts:

- `README.md` — learning goals, prereqs, concepts, exercise brief, how to run, going further.
- `slides/` — `index.html` (reveal.js bootstrap), `slides.md` (markdown), `assets/`.
- `exercises/` — runnable but incomplete code + failing `test_*.py` tests that are the spec.
- `solutions/` — fully-implemented reference; tests must match `exercises/`.

The scaffolder creates all four with sensible placeholders.

## Slide style

- Markdown with HTML escape hatches; `---` separates horizontal slides, `--` separates vertical ones (used sparingly).
- Code-heavy slides: keep to ~15 visible lines. Split longer examples across slides.
- First slide: lesson number, title, one-line learning goal. Last slide: pointer to the next lesson.
- Diagrams: SVG only. Never images of code.
- Speaker notes via `Note:` blocks at the bottom of a slide.

## Code style

- `make fmt` before committing.
- `make lint` and `make typecheck` must pass.
- Type hints are required from lesson 9 onward; earlier lessons stay un-typed by design.

## Commit messages

Conventional Commits: `feat(lesson-04): ...`, `fix(slides_dev): ...`, `docs: ...`, etc.

## Tests as spec

`exercises/test_*.py` files define what "done" means. Students make those tests pass; the solutions/ copy must keep the same tests green. Drift between the two is caught in CI.
````

- [ ] **Step 2: Refresh `README.md`**

Replace the existing `README.md` content with:

````markdown
# Python Training

A Python programming course delivered as code + per-lesson reveal.js slide decks.
The arc starts at programming-101 and finishes with async, typing, web services,
packaging, observability, and deployment.

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) (manages the Python toolchain and venv):
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- Make
- Docker (only for `make slides-docker`, added in a later plan)

`uv` reads `.python-version` and installs the right Python automatically — no
separate `pyenv` or system Python step needed.

## Quick start

Clone the repo, then from the repo root:

```bash
make help                       # list every available command
make sync                       # install the workspace into .venv
make new-lesson NAME=99-demo    # scaffold a sandbox lesson
make slides-dev LESSON=99-demo  # serve its deck on http://localhost:8000
make test                       # run all solution tests
```

## Repository layout

```
lessons/NN-name/
├── pyproject.toml  workspace member; per-lesson deps live here
├── README.md       self-study notes for the lesson
├── slides/         reveal.js deck (index.html + slides.md)
├── exercises/      starter code + failing tests (the spec)
└── solutions/      reference implementation

shared/reveal/      vendored reveal.js + custom theme (do not edit by hand)
tools/              developer tooling (new_lesson, slides_dev, build_index)
docs/               design docs and implementation plans
```

## Design

See [`docs/superpowers/specs/2026-05-25-python-course-design.md`](docs/superpowers/specs/2026-05-25-python-course-design.md)
for the course design.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the lesson conventions and dev workflow.
````

> The README already contains the same content; the only delta vs. the existing file is the added "Contributing" link. If the diff is empty after editing, skip the file change and just add CONTRIBUTING.md.

- [ ] **Step 3: Commit**

```bash
git add CONTRIBUTING.md README.md
git commit -m "docs: add CONTRIBUTING.md and link from README"
```

---

## Task 13: End-to-end smoke test

Confirm the whole bootstrap works the way the README promises.

- [ ] **Step 1: From a clean checkout, sync and check `make help`**

Run: `make help`
Expected: lists every Make target.

- [ ] **Step 2: Scaffold a sandbox lesson**

Run: `make new-lesson NAME=99-demo`
Expected: prints `created lessons/99-demo`. Directory exists with `README.md`, `pyproject.toml`, `slides/index.html`, `slides/slides.md`, `exercises/main.py`, `exercises/test_main.py`, `solutions/main.py`, `solutions/test_main.py`.

- [ ] **Step 3: Sync (picks up the new workspace member)**

Run: `make sync`
Expected: uv updates `uv.lock` to include `lesson-99-demo` and exits 0.

- [ ] **Step 4: Solution tests pass; exercise tests fail by design**

Run: `make test-lesson LESSON=99-demo`
Expected: exercises FAIL with `NotImplementedError`, solutions pass. Exit code is 0 (the Makefile target swallows the exercise failure via `-`).

- [ ] **Step 5: Slides dev server starts**

Run: `make slides-dev LESSON=99-demo` in the background (e.g., `make slides-dev LESSON=99-demo &`) or in a second terminal.

Then in the foreground:
```bash
curl -s http://127.0.0.1:8000/ | head -3
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/slides.md
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/shared/reveal/dist/reveal.css
```

Expected:
- First `curl` returns the lesson's `index.html` (contains `<title>Lesson 99`).
- Second `curl` returns `200`.
- Third `curl` returns `200`.

Stop the dev server (Ctrl-C, or `kill %1` if backgrounded).

- [ ] **Step 6: Tear down the sandbox**

```bash
rm -rf lessons/99-demo
uv sync
```

Expected: `lessons/99-demo` is gone; uv removes the workspace member from the lock cleanly.

- [ ] **Step 7: Run the full quality bar one last time**

```bash
make lint
make typecheck
make test
```

Expected: all three exit 0.

- [ ] **Step 8: Commit the smoke-test-clean state (only if files changed)**

```bash
git status
```

If `git status` shows changes, commit them:
```bash
git add -A
git commit -m "chore: tidy after end-to-end smoke test"
```

If clean, skip.

- [ ] **Step 9: Push to origin**

```bash
git push origin main
```

Expected: GitHub accepts the push; the branch is up to date.
```
