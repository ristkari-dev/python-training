# Plan B — Slides Build & Deploy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the static slide-site builder (`tools/build_index`), wire `make slides-build` / `make slides-docker`, and ship the full deploy story (two-stage Docker image, Cloud Run config, idempotent GCP bootstrap, and GitHub Actions CI + deploy) so a push to `main` publishes the decks at `https://python.ristkari.dev/`.

**Architecture:** `build_index` is a third uv-workspace member (alongside `new_lesson` and `slides_dev`), stdlib-only, with a `src/` layout. It holds a master catalog of all 28 lessons; lessons whose `slides/` directory exists on disk render as links, the rest as faded "future" placeholders, so the landing page is complete from day one and CI has stable content to assert against. The deploy path mirrors the sibling `rust-training` / `elixir-training` repos exactly, with python-augmented resource names: a two-stage Dockerfile (uv builder → `nginx-unprivileged` runtime) produces a static `dist/`, pushed to Artifact Registry and deployed to Cloud Run via Workload Identity Federation (no long-lived keys).

**Tech Stack:** Python 3.13, `uv`, stdlib (`pathlib`, `shutil`, `argparse`, `html`), `nginx-unprivileged`, Docker, Google Cloud Run + Artifact Registry, GitHub Actions, GCP Workload Identity Federation.

---

## Context for the implementer

- **Repo state:** Plan A is merged to `main`. The repo has a working uv workspace with two tools (`tools/new_lesson`, `tools/slides_dev`), vendored reveal.js at `shared/reveal/`, a custom theme `shared/reveal/theme/python-training.css`, and a Makefile. `lessons/` is currently EMPTY (no lessons authored yet) — this is expected and the build must handle it gracefully.
- **Sibling repos to mirror:** `/Users/ristkari/code/private/rust-training/` and `/Users/ristkari/code/private/elixir-training/` already implement this exact deploy pattern. Their `deploy/` files and `tools/build-index` (Rust) / `tools/build_index/build_index.exs` (Elixir) are the reference. This plan ports that pattern to Python; you generally do NOT need to read those repos because the full content is inlined below, but they're available if a detail is ambiguous.
- **`make sync` uses `uv sync --all-packages`** (workspace root is `package = false`, so plain `uv sync` does not install members). After creating the new `build_index` member, run `uv sync --all-packages`.
- **The build tool is stdlib-only** (no third-party deps) but is still a workspace member so it's importable, testable, and consistent with the other two tools. mypy `--strict` applies to `tools/build_index/src`.

## Conventions used by this plan

- **Working directory:** `/Users/ristkari/code/private/python-training/` for every command.
- **Commit messages:** Conventional Commits (`feat:`, `build:`, `ci:`, `test:`, `docs:`).
- **GCP resource names (python-augmented, shared `ristkari-dev` project):**
  - Region: `europe-north1`
  - Artifact Registry repo: `python-training`
  - Cloud Run service: `python-training-slides`
  - Deploy service account: `github-deploy-python@ristkari-dev.iam.gserviceaccount.com`
  - WIF pool: `github-actions` (shared, already exists from sibling repos)
  - WIF provider: `github-python-training` (repo-suffixed; the pool is shared, each provider is scoped to one repo)
  - GitHub repo: `ristkari-dev/python-training`
  - Custom domain: `python.ristkari.dev` (Cloudflare CNAME → `ghs.googlehosted.com`, DNS-only)
- **Do NOT push or run any `gcloud` commands.** This plan only writes files and runs local builds/tests. The actual GCP bootstrap (`./deploy/setup.sh`), secret-setting, and DNS are the owner's manual one-time steps, documented in `deploy/README.md`.

---

## File Structure

After this plan completes, the repo gains:

```
python-training/
├── Makefile                                   (MODIFY: add slides-build, slides-docker)
├── tools/
│   └── build_index/                           (NEW workspace member)
│       ├── pyproject.toml
│       ├── src/
│       │   └── build_index/
│       │       ├── __init__.py
│       │       ├── catalog.py                 (LessonInfo, PHASES, ALL_LESSONS — 28 lessons)
│       │       ├── template.py                (INDEX_HEAD / INDEX_TAIL HTML constants)
│       │       ├── builder.py                 (collect_published, copy_tree, render_index, build)
│       │       └── __main__.py                (argparse CLI)
│       └── tests/
│           ├── test_catalog.py
│           └── test_builder.py
├── deploy/                                     (NEW)
│   ├── Dockerfile
│   ├── nginx.conf.template
│   ├── cloudrun.yaml
│   ├── setup.sh
│   └── README.md
└── .github/
    └── workflows/                              (NEW)
        ├── ci.yml
        └── deploy.yml
```

### Decomposition rationale

- `catalog.py` is pure data (the lesson list) so editing the curriculum never touches logic.
- `template.py` isolates the large HTML+CSS blob so `builder.py` stays focused on filesystem + rendering logic and is easy to read in one screen.
- `builder.py` holds the four testable functions; `__main__.py` is thin CLI wiring.
- Tests split by concern: catalog integrity vs. build behaviour.

---

## Task 1: Scaffold the `build_index` workspace member

**Files:**
- Create: `tools/build_index/pyproject.toml`
- Create: `tools/build_index/src/build_index/__init__.py`

- [ ] **Step 1: Create `tools/build_index/pyproject.toml`**

```toml
[project]
name = "build-index"
version = "0.0.0"
description = "Static-site generator for the python-training slide decks"
requires-python = ">=3.13"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/build_index"]
```

- [ ] **Step 2: Create `tools/build_index/src/build_index/__init__.py`**

```python
"""Static-site generator for the python-training slide decks."""
```

- [ ] **Step 3: Sync the workspace**

Run: `uv sync --all-packages`
Expected: uv installs `build-index` into the workspace venv, exits 0.

- [ ] **Step 4: Verify import**

Run: `uv run python -c "import build_index; print(build_index.__doc__)"`
Expected: prints `Static-site generator for the python-training slide decks.`

- [ ] **Step 5: Commit**

```bash
git add tools/build_index/pyproject.toml tools/build_index/src uv.lock
git commit -m "feat(build_index): add workspace member skeleton"
```

---

## Task 2: Add the lesson catalog with tests

**Files:**
- Create: `tools/build_index/src/build_index/catalog.py`
- Create: `tools/build_index/tests/test_catalog.py`

The catalog is the master list of all 28 lessons across 4 phases, from the course design spec (`docs/superpowers/specs/2026-05-25-python-course-design.md`). Published-or-not is determined at build time by disk; the catalog itself lists every lesson.

- [ ] **Step 1: Write the failing test**

Path: `tools/build_index/tests/test_catalog.py`

```python
from build_index.catalog import ALL_LESSONS, PHASES, LessonInfo


def test_has_28_lessons() -> None:
    assert len(ALL_LESSONS) == 28


def test_lesson_numbers_are_sequential_two_digit() -> None:
    numbers = [lesson.number for lesson in ALL_LESSONS]
    assert numbers == [f"{i:02d}" for i in range(1, 29)]


def test_four_phases_defined() -> None:
    phase_nums = [num for num, _name in PHASES]
    assert phase_nums == [1, 2, 3, 4]


def test_every_lesson_phase_exists_in_phases() -> None:
    defined = {num for num, _name in PHASES}
    for lesson in ALL_LESSONS:
        assert lesson.phase in defined


def test_phase_boundaries() -> None:
    # Phase 1: lessons 1-8, Phase 2: 9-15, Phase 3: 16-21, Phase 4: 22-28
    by_number = {lesson.number: lesson.phase for lesson in ALL_LESSONS}
    assert by_number["01"] == 1
    assert by_number["08"] == 1
    assert by_number["09"] == 2
    assert by_number["15"] == 2
    assert by_number["16"] == 3
    assert by_number["21"] == 3
    assert by_number["22"] == 4
    assert by_number["28"] == 4


def test_slugs_are_kebab_case() -> None:
    import re

    pattern = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
    for lesson in ALL_LESSONS:
        assert pattern.match(lesson.slug), f"bad slug: {lesson.slug!r}"


def test_dir_name_combines_number_and_slug() -> None:
    first = ALL_LESSONS[0]
    assert first.dir_name() == f"{first.number}-{first.slug}"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `uv run pytest tools/build_index/tests/test_catalog.py -v`
Expected: collection error / `ModuleNotFoundError: No module named 'build_index.catalog'`.

- [ ] **Step 3: Implement `catalog.py`**

Path: `tools/build_index/src/build_index/catalog.py`

```python
"""The master catalog of every lesson in the course.

Editing this list is how a lesson appears on the landing page: it shows as a
faded "future" placeholder until the matching ``lessons/NN-slug/slides/``
directory lands on disk, at which point it lights up as a link.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LessonInfo:
    number: str
    slug: str
    title: str
    blurb: str
    phase: int

    def dir_name(self) -> str:
        """Full lesson directory name, e.g. ``01-hello``."""
        return f"{self.number}-{self.slug}"


PHASES: tuple[tuple[int, str], ...] = (
    (1, "Foundations"),
    (2, "Idiomatic Python"),
    (3, "Async, Concurrency & Tooling"),
    (4, "Production & Services"),
)


ALL_LESSONS: tuple[LessonInfo, ...] = (
    # Phase 1 — Foundations
    LessonInfo("01", "hello", "Hello, Python", "uv · python -m · print · pytest", 1),
    LessonInfo("02", "variables", "Variables, types, operators", "int·float·str·bool·None · f-strings", 1),
    LessonInfo("03", "control-flow", "Control flow", "if·elif · for · while · match", 1),
    LessonInfo("04", "functions", "Functions & tests", "args · *args·**kwargs · pytest", 1),
    LessonInfo("05", "collections", "Collections", "list·tuple·dict·set · comprehensions", 1),
    LessonInfo("06", "classes", "Classes & dataclasses", "__init__ · @dataclass · dunders", 1),
    LessonInfo("07", "modules", "Modules, packages, imports", "__init__.py · imports · stdlib", 1),
    LessonInfo("08", "capstone-cli", "Phase 1 capstone — CLI", "argparse · files · multi-module", 1),
    # Phase 2 — Idiomatic Python
    LessonInfo("09", "type-hints", "Type hints & mypy", "list[int] · Optional · TypedDict", 2),
    LessonInfo("10", "protocols", "Protocols, ABCs, duck typing", "Protocol · abc.ABC · structural", 2),
    LessonInfo("11", "errors", "Errors & exceptions", "try·except · custom · raise from", 2),
    LessonInfo("12", "iterators", "Iterators & generators", "yield · itertools · gen exprs", 2),
    LessonInfo("13", "decorators", "Decorators & context managers", "@decorator · with · contextlib", 2),
    LessonInfo("14", "files-json-dates", "Files, JSON, paths, dates", "pathlib · json · datetime · zoneinfo", 2),
    LessonInfo("15", "structure", "Project structure & testing", "src/ · pyproject · fixtures", 2),
    # Phase 3 — Async, Concurrency & Tooling
    LessonInfo("16", "threads", "Concurrency & threads", "GIL · threading · when not to", 3),
    LessonInfo("17", "multiprocessing", "Multiprocessing & futures", "pools · concurrent.futures", 3),
    LessonInfo("18", "asyncio", "asyncio basics", "async·await · event loop", 3),
    LessonInfo("19", "async-patterns", "Async patterns", "gather · TaskGroup · cancellation", 3),
    LessonInfo("20", "http-clients", "HTTP clients & resilience", "httpx · retries · tenacity", 3),
    LessonInfo("21", "profiling", "Profiling & debugging", "cProfile · pyinstrument · pdb", 3),
    # Phase 4 — Production & Services
    LessonInfo("22", "fastapi", "FastAPI fundamentals", "routing · Pydantic · DI · middleware", 4),
    LessonInfo("23", "fastapi-testing", "FastAPI testing & validation", "TestClient · Pydantic v2", 4),
    LessonInfo("24", "databases", "Databases with SQLAlchemy 2", "engine · session · Alembic", 4),
    LessonInfo("25", "config", "Configuration & settings", "pydantic-settings · 12-factor", 4),
    LessonInfo("26", "packaging", "Build, package, containerize", "uv build · wheels · Dockerfile", 4),
    LessonInfo("27", "observability", "Observability", "structured logs · OpenTelemetry", 4),
    LessonInfo("28", "distributed", "Distributed patterns & wrap-up", "queues · idempotency · capstone", 4),
)
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `uv run pytest tools/build_index/tests/test_catalog.py -v`
Expected: all 7 tests pass.

- [ ] **Step 5: Format, lint, and type-check**

Several `LessonInfo(...)` rows are written on one line above for readability and exceed the 100-char limit. `ruff format` auto-wraps any over-long call across multiple lines, so run it FIRST, then `ruff check` will pass.

Run: `uv run ruff format tools/build_index`
Expected: reformats `catalog.py` (wrapping the long rows); prints e.g. `2 files reformatted` or `left unchanged`.

Run: `uv run ruff check tools/build_index`
Expected: All checks passed!

Run: `uv run mypy tools/build_index/src`
Expected: Success.

Re-run the catalog tests after formatting to confirm nothing broke:

Run: `uv run pytest tools/build_index/tests/test_catalog.py -q`
Expected: 7 passed.

- [ ] **Step 6: Commit**

```bash
git add tools/build_index/src/build_index/catalog.py tools/build_index/tests/test_catalog.py
git commit -m "feat(build_index): add 28-lesson catalog with integrity tests"
```

---

## Task 3: Add the HTML template constants

**Files:**
- Create: `tools/build_index/src/build_index/template.py`

This module holds the Python-branded landing-page HTML head/tail as string constants. The palette matches the slide theme (`--python-blue #3776AB`, `--python-yellow #FFD43B`) on a dark background. `builder.py` (Task 4) concatenates `INDEX_HEAD + <generated body> + INDEX_TAIL`.

- [ ] **Step 1: Create `tools/build_index/src/build_index/template.py`**

```python
"""HTML head/tail constants for the generated landing page.

The body (phase headers + lesson cards) is generated in ``builder.py`` and
inserted between ``INDEX_HEAD`` and ``INDEX_TAIL``.
"""

INDEX_HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Python Training</title>
  <style>
    :root {
      --bg: #0f1722;
      --surface: #16212e;
      --border: rgba(55, 118, 171, 0.30);

      --fg: #e8eef5;
      --fg-muted: rgba(232, 238, 245, 0.65);
      --fg-subtle: rgba(232, 238, 245, 0.42);

      --python-blue: #4b8bbe;
      --python-yellow: #ffd43b;
      --accent: var(--python-yellow);
      --accent-soft: rgba(75, 139, 190, 0.12);
      --accent-strong: rgba(255, 212, 59, 0.55);

      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: "JetBrains Mono", "SF Mono", "Source Code Pro", Menlo, Consolas, monospace;
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; background: var(--bg); color: var(--fg); }
    body { font-family: var(--font-sans); font-size: 16px; line-height: 1.55; }

    main { max-width: 960px; margin: 0 auto; padding: 60px 28px 100px; }

    h1 {
      font-size: 2.6rem;
      font-weight: 700;
      color: var(--python-yellow);
      letter-spacing: -0.025em;
      margin: 0 0 0.3rem;
    }
    p.lead {
      font-size: 1.1rem;
      color: var(--fg-muted);
      margin: 0 0 2.5rem;
      max-width: 640px;
    }

    .phase {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--python-blue);
      margin: 2.5rem 0 1rem;
      display: flex;
      align-items: center;
      gap: 0.7rem;
    }
    .phase::after {
      content: "";
      flex: 1;
      height: 1px;
      background: var(--border);
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 0.7rem;
    }

    .lesson {
      background: var(--accent-soft);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.95rem 1rem 1rem;
      text-decoration: none;
      color: inherit;
      transition: transform 150ms ease, border-color 150ms ease, background 150ms ease;
      display: block;
    }
    .lesson:hover {
      transform: translateY(-2px);
      border-color: var(--accent-strong);
      background: rgba(75, 139, 190, 0.18);
    }
    .lesson:focus-visible {
      outline: 2px solid var(--python-yellow);
      outline-offset: 3px;
    }
    .lesson .num {
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 600;
      color: var(--python-yellow);
      letter-spacing: 0.05em;
    }
    .lesson .title {
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--fg);
      letter-spacing: -0.01em;
      margin-top: 0.25rem;
      line-height: 1.25;
    }
    .lesson .blurb {
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--fg-muted);
      margin-top: 0.45rem;
      line-height: 1.4;
    }

    .lesson.future {
      background: rgba(255, 255, 255, 0.02);
      border: 1px dashed rgba(255, 255, 255, 0.08);
      opacity: 0.42;
      cursor: default;
    }
    .lesson.future:hover {
      transform: none;
      background: rgba(255, 255, 255, 0.02);
      border-color: rgba(255, 255, 255, 0.08);
    }
    .lesson.future .num,
    .lesson.future .title { color: var(--fg-muted); }
    .lesson.future .blurb { color: var(--fg-subtle); }

    footer {
      margin-top: 4rem;
      padding-top: 1.5rem;
      border-top: 1px solid rgba(255,255,255,0.06);
      font-size: 0.9rem;
      color: var(--fg-subtle);
    }
    footer a { color: var(--python-yellow); text-decoration: none; }
    footer a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <main>
    <h1>Python Training</h1>
    <p class="lead">A Python programming course delivered as code + per-lesson reveal.js slide decks. Starts at programming-101 and finishes with async, typing, web services, packaging, observability, and deployment.</p>

"""


INDEX_TAIL = """
    <footer>
      Source: <a href="https://github.com/ristkari-dev/python-training">github.com/ristkari-dev/python-training</a>
    </footer>
  </main>
</body>
</html>
"""
```

- [ ] **Step 2: Verify the module imports and constants are non-empty**

Run: `uv run python -c "from build_index.template import INDEX_HEAD, INDEX_TAIL; print('Python Training' in INDEX_HEAD, INDEX_TAIL.strip().endswith('</html>'))"`
Expected: `True True`

- [ ] **Step 3: Lint and type-check**

Run: `uv run ruff check tools/build_index`
Expected: All checks passed!

Run: `uv run mypy tools/build_index/src`
Expected: Success.

- [ ] **Step 4: Commit**

```bash
git add tools/build_index/src/build_index/template.py
git commit -m "feat(build_index): add Python-branded landing-page HTML template"
```

---

## Task 4: Implement the builder with tests

**Files:**
- Create: `tools/build_index/src/build_index/builder.py`
- Create: `tools/build_index/tests/test_builder.py`

Four functions:
- `escape_html(s) -> str` — escape `&`, `<`, `>`.
- `collect_published(lessons_dir: Path) -> set[str]` — directory names under `lessons_dir` that contain a `slides/` subdir; empty set if `lessons_dir` is missing.
- `copy_tree(src: Path, dst: Path) -> None` — recursive file copy, creating dirs; no-op if `src` missing.
- `render_index(published: set[str]) -> str` — `INDEX_HEAD` + phase/lesson body + `INDEX_TAIL`; published lessons become `<a>` links, others `<div class="lesson future">`.
- `build(lessons_dir, shared_dir, out_dir) -> None` — clears `out_dir`, copies each published lesson's `slides/` to `out_dir/lessons/<name>/slides/`, copies `shared_dir` to `out_dir/shared/reveal/`, writes `out_dir/index.html`.

- [ ] **Step 1: Write the failing tests**

Path: `tools/build_index/tests/test_builder.py`

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tools/build_index/tests/test_builder.py -v`
Expected: collection error / `ModuleNotFoundError: No module named 'build_index.builder'`.

- [ ] **Step 3: Implement `builder.py`**

Path: `tools/build_index/src/build_index/builder.py`

```python
"""Filesystem operations and HTML rendering for the static slide site."""

from __future__ import annotations

import shutil
from pathlib import Path

from build_index.catalog import ALL_LESSONS, PHASES, LessonInfo
from build_index.template import INDEX_HEAD, INDEX_TAIL


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def collect_published(lessons_dir: Path) -> set[str]:
    """Directory names under lessons_dir that contain a slides/ subdir.

    Returns an empty set if lessons_dir does not exist — the normal state for
    a fresh checkout with no lessons authored yet.
    """
    if not lessons_dir.is_dir():
        return set()
    return {
        entry.name
        for entry in lessons_dir.iterdir()
        if entry.is_dir() and (entry / "slides").is_dir()
    }


def copy_tree(src: Path, dst: Path) -> None:
    """Recursively copy src into dst, creating directories as needed.

    No-op if src does not exist.
    """
    if not src.exists():
        return
    for entry in sorted(src.rglob("*")):
        rel = entry.relative_to(src)
        target = dst / rel
        if entry.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif entry.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry, target)


def render_index(published: set[str]) -> str:
    """Render the landing page: published lessons link, others are faded."""
    body_parts: list[str] = []
    for phase_num, phase_name in PHASES:
        body_parts.append(
            f'    <div class="phase">Phase {phase_num} · {escape_html(phase_name)}</div>\n'
        )
        body_parts.append('    <div class="grid">\n')
        for lesson in ALL_LESSONS:
            if lesson.phase != phase_num:
                continue
            body_parts.append(_render_lesson(lesson, published))
        body_parts.append("    </div>\n")
    return INDEX_HEAD + "".join(body_parts) + INDEX_TAIL


def _render_lesson(lesson: LessonInfo, published: set[str]) -> str:
    title = escape_html(lesson.title)
    blurb = escape_html(lesson.blurb)
    number = lesson.number
    dir_name = lesson.dir_name()
    if dir_name in published:
        return (
            f'      <a class="lesson" href="lessons/{dir_name}/slides/">\n'
            f'        <div class="num">{number}</div>\n'
            f'        <div class="title">{title}</div>\n'
            f'        <div class="blurb">{blurb}</div>\n'
            f"      </a>\n"
        )
    return (
        '      <div class="lesson future" aria-disabled="true">\n'
        f'        <div class="num">{number}</div>\n'
        f'        <div class="title">{title}</div>\n'
        f'        <div class="blurb">{blurb}</div>\n'
        f"      </div>\n"
    )


def build(lessons_dir: Path, shared_dir: Path, out_dir: Path) -> None:
    """Clear out_dir, copy published slides + shared assets, write index.html."""
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    published = collect_published(lessons_dir)
    for name in published:
        copy_tree(lessons_dir / name / "slides", out_dir / "lessons" / name / "slides")

    copy_tree(shared_dir, out_dir / "shared" / "reveal")

    (out_dir / "index.html").write_text(render_index(published), encoding="utf-8")
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `uv run pytest tools/build_index/tests/test_builder.py -v`
Expected: all tests pass (1 + 3 + 2 + 4 + 3 = 13 tests).

- [ ] **Step 5: Lint and type-check**

Run: `uv run ruff check tools/build_index`
Expected: All checks passed!

Run: `uv run mypy tools/build_index/src`
Expected: Success.

- [ ] **Step 6: Commit**

```bash
git add tools/build_index/src/build_index/builder.py tools/build_index/tests/test_builder.py
git commit -m "feat(build_index): implement collect_published, copy_tree, render_index, build"
```

---

## Task 5: Add the `build_index` CLI

**Files:**
- Create: `tools/build_index/src/build_index/__main__.py`

- [ ] **Step 1: Write the CLI**

Path: `tools/build_index/src/build_index/__main__.py`

```python
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
```

- [ ] **Step 2: Smoke-test `--help`**

Run: `uv run python -m build_index --help`
Expected: argparse prints usage with `--lessons`, `--shared`, `--out`. Exit 0.

- [ ] **Step 3: Smoke-test a real build (zero lessons currently)**

Run: `uv run python -m build_index --out /tmp/pt-dist-smoke`
Expected: prints `built /tmp/pt-dist-smoke`. Then:

```bash
test -f /tmp/pt-dist-smoke/index.html && echo "index ok"
grep -q "Python Training" /tmp/pt-dist-smoke/index.html && echo "title ok"
grep -c 'class="lesson future"' /tmp/pt-dist-smoke/index.html   # expect 28
test -f /tmp/pt-dist-smoke/shared/reveal/dist/reveal.css && echo "reveal copied"
rm -rf /tmp/pt-dist-smoke
```
Expected: `index ok`, `title ok`, `28`, `reveal copied`.

- [ ] **Step 4: Lint and type-check**

Run: `uv run ruff check tools/build_index`
Expected: All checks passed!

Run: `uv run mypy tools/build_index/src`
Expected: Success.

- [ ] **Step 5: Commit**

```bash
git add tools/build_index/src/build_index/__main__.py
git commit -m "feat(build_index): add CLI entry point"
```

---

## Task 6: Wire `slides-build` and `slides-docker` into the Makefile

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Read the current Makefile**

Run: `cat Makefile` — note the existing targets (`help`, `sync`, `test`, `test-exercises`, `test-lesson`, `lint`, `fmt`, `typecheck`, `new-lesson`, `slides-dev`) and that recipes use TAB indentation.

- [ ] **Step 2: Append the two new targets**

Add these targets to `Makefile` (after `slides-dev`, before EOF). Recipe lines MUST use real TABs.

```makefile
.PHONY: slides-build
slides-build: ## Build the static slides site into dist/
	uv run python -m build_index --lessons lessons --shared shared/reveal --out dist

.PHONY: slides-docker
slides-docker: ## Build the deploy image and run it locally on http://localhost:8080
	docker build -t python-training-slides:local -f deploy/Dockerfile .
	@echo "starting container on http://localhost:8080  (Ctrl-C to stop)"
	docker run --rm -p 8080:8080 -e PORT=8080 python-training-slides:local
```

- [ ] **Step 3: Verify the targets are listed and `slides-build` works**

Run: `make help | grep -E 'slides-build|slides-docker'`
Expected: both lines appear with descriptions.

Run: `make slides-build`
Expected: prints `built dist`. Then:

```bash
test -f dist/index.html && grep -q "Python Training" dist/index.html && echo "dist ok"
```
Expected: `dist ok`.

- [ ] **Step 4: Confirm `dist/` is gitignored**

Run: `git status --porcelain dist/`
Expected: NO output (dist/ is already ignored by the `.gitignore` `dist/` rule from Plan A; the `!shared/reveal/dist/` negation only un-ignores the vendored tree, not the generated `dist/`). If `dist/` shows as untracked, STOP and report — the gitignore needs checking.

- [ ] **Step 5: Clean the build artifact and commit only the Makefile**

```bash
rm -rf dist
git add Makefile
git commit -m "build: add slides-build and slides-docker make targets"
```

---

## Task 7: Add the deploy Dockerfile

**Files:**
- Create: `deploy/Dockerfile`

Two stages: a `python:3.13-slim` builder that installs `uv`, syncs the workspace, and runs `build_index` to produce `/dist`; then an `nginx-unprivileged` runtime that serves `/dist`. The runtime image contains no Python.

- [ ] **Step 1: Create `deploy/Dockerfile`**

```dockerfile
# syntax=docker/dockerfile:1.7

# --- Stage 1: build the static dist/ ---
FROM python:3.13-slim AS builder
WORKDIR /src

# uv: copy the static binary from the official image (no curl/install step).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the whole repo; build_index needs lessons/, shared/, and the tool.
COPY . .

# Install the workspace (members include build_index) without dev tools,
# then render the landing page + copy decks + vendored reveal.js into /dist.
RUN uv sync --frozen --all-packages --no-dev \
    && uv run --no-dev --all-packages python -m build_index \
        --lessons /src/lessons \
        --shared /src/shared/reveal \
        --out /dist

# --- Stage 2: serve dist/ with non-root nginx ---
FROM nginxinc/nginx-unprivileged:alpine
USER root
COPY deploy/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=builder /dist /usr/share/nginx/html
# Drop back to the unprivileged user the image ships with (UID 101).
USER 101
EXPOSE 8080
```

> **Why `--frozen`:** fails the build if `uv.lock` is out of date rather than silently resolving — keeps the image reproducible. **Why `--no-dev`:** ruff/mypy/pytest aren't needed to build the static site; `build_index` is a regular workspace member (not a dev dependency) so it's still installed.

- [ ] **Step 2: Lint the Dockerfile syntax (best-effort)**

Run: `grep -q "nginx-unprivileged" deploy/Dockerfile && grep -q "build_index" deploy/Dockerfile && echo "dockerfile shape ok"`
Expected: `dockerfile shape ok`. (A full `docker build` is exercised in Task 13.)

- [ ] **Step 3: Commit**

```bash
git add deploy/Dockerfile
git commit -m "build: add two-stage deploy Dockerfile (uv builder -> nginx runtime)"
```

---

## Task 8: Add the nginx config template

**Files:**
- Create: `deploy/nginx.conf.template`

`nginx-unprivileged` substitutes `${PORT}` from the environment at container start (Cloud Run injects `PORT`, default 8080). Static assets cache for an hour; HTML/markdown are no-cache so deploys propagate immediately.

- [ ] **Step 1: Create `deploy/nginx.conf.template`**

```nginx
server {
    listen ${PORT} default_server;
    listen [::]:${PORT} default_server;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Static assets: cache for an hour
    location ~* \.(?:js|mjs|css|svg|woff2?|ttf|otf|png|jpg|jpeg|gif|ico|map)$ {
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
        try_files $uri =404;
    }

    # HTML and markdown: no cache (so deploys propagate immediately)
    location ~* \.(?:html|md)$ {
        add_header Cache-Control "no-cache";
        try_files $uri =404;
    }

    # Default: try the file, then a directory's index.html, else 404
    location / {
        try_files $uri $uri/ =404;
    }

    # Favicon shouldn't 404 noisily if missing
    location = /favicon.ico {
        log_not_found off;
        access_log off;
    }
}
```

- [ ] **Step 2: Commit**

```bash
git add deploy/nginx.conf.template
git commit -m "build: add nginx config template for the slides runtime"
```

---

## Task 9: Add the Cloud Run service spec

**Files:**
- Create: `deploy/cloudrun.yaml`

A Knative-style service definition checked in for reproducibility. `__IMAGE__` is replaced by the deploy workflow with the freshly-pushed image reference.

- [ ] **Step 1: Create `deploy/cloudrun.yaml`**

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: python-training-slides
  labels:
    cloud.googleapis.com/location: europe-north1
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "0"
        autoscaling.knative.dev/maxScale: "2"
        run.googleapis.com/cpu-throttling: "true"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 30
      containers:
        - image: __IMAGE__
          ports:
            - name: http1
              containerPort: 8080
          resources:
            limits:
              cpu: "1"
              memory: 256Mi
  traffic:
    - percent: 100
      latestRevision: true
```

- [ ] **Step 2: Commit**

```bash
git add deploy/cloudrun.yaml
git commit -m "build: add Cloud Run service spec (python-training-slides)"
```

---

## Task 10: Add the idempotent GCP bootstrap script

**Files:**
- Create: `deploy/setup.sh` (executable)

Re-runnable `gcloud` bootstrap: enables APIs, creates the Artifact Registry repo, the deploy service account + roles, the WIF pool (shared) + a repo-scoped OIDC provider, and binds the repo to impersonate the SA. Prints the three GitHub secrets to set.

- [ ] **Step 1: Create `deploy/setup.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail

# Idempotent GCP bootstrap for the python-training slides deployment.
# Re-runnable: each step either creates the resource or no-ops if it already exists.

PROJECT_ID="${PROJECT_ID:-ristkari-dev}"
REGION="${REGION:-europe-north1}"
AR_REPO="${AR_REPO:-python-training}"
SERVICE_NAME="${SERVICE_NAME:-python-training-slides}"
SA_NAME="${SA_NAME:-github-deploy-python}"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
WIF_POOL="${WIF_POOL:-github-actions}"
# Provider names must be unique-per-repo within the shared pool, because each
# provider has its own attribute condition restricting which GitHub repo can
# impersonate. Sibling repos own their own providers; use a repo-suffixed name.
WIF_PROVIDER="${WIF_PROVIDER:-github-python-training}"
GITHUB_REPO="${GITHUB_REPO:-ristkari-dev/python-training}"

bold()  { printf '\033[1m%s\033[0m\n' "$*"; }
note()  { printf '  → %s\n' "$*"; }

bold "Project:        $PROJECT_ID"
bold "Region:         $REGION"
bold "AR repo:        $AR_REPO"
bold "Service:        $SERVICE_NAME"
bold "Service acct:   $SA_EMAIL"
bold "WIF pool:       $WIF_POOL"
bold "WIF provider:   $WIF_PROVIDER"
bold "GitHub repo:    $GITHUB_REPO"
echo

bold "1. Enabling required APIs"
gcloud services enable \
    artifactregistry.googleapis.com \
    iamcredentials.googleapis.com \
    run.googleapis.com \
    sts.googleapis.com \
    --project="$PROJECT_ID"

bold "2. Creating Artifact Registry repo (if missing)"
if gcloud artifacts repositories describe "$AR_REPO" \
        --location="$REGION" --project="$PROJECT_ID" >/dev/null 2>&1; then
    note "repo $AR_REPO already exists, skipping"
else
    gcloud artifacts repositories create "$AR_REPO" \
        --repository-format=docker \
        --location="$REGION" \
        --description="python-training container images" \
        --project="$PROJECT_ID"
fi

bold "3. Creating service account (if missing)"
if gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT_ID" >/dev/null 2>&1; then
    note "service account $SA_EMAIL already exists, skipping"
else
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="GitHub Actions deploy for python-training" \
        --project="$PROJECT_ID"
fi

bold "4. Granting roles to the service account"
for role in \
    roles/artifactregistry.writer \
    roles/run.admin \
    roles/iam.serviceAccountUser \
; do
    note "binding $role"
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:$SA_EMAIL" \
        --role="$role" \
        --condition=None \
        --quiet >/dev/null
done

bold "5. Creating Workload Identity Federation pool (if missing)"
if gcloud iam workload-identity-pools describe "$WIF_POOL" \
        --location=global --project="$PROJECT_ID" >/dev/null 2>&1; then
    note "pool $WIF_POOL already exists, skipping"
else
    gcloud iam workload-identity-pools create "$WIF_POOL" \
        --location=global \
        --display-name="GitHub Actions" \
        --project="$PROJECT_ID"
fi

POOL_NAME=$(gcloud iam workload-identity-pools describe "$WIF_POOL" \
    --location=global --project="$PROJECT_ID" --format='value(name)')

bold "6. Creating WIF OIDC provider for GitHub (if missing)"
if gcloud iam workload-identity-pools providers describe "$WIF_PROVIDER" \
        --location=global --workload-identity-pool="$WIF_POOL" \
        --project="$PROJECT_ID" >/dev/null 2>&1; then
    note "provider $WIF_PROVIDER already exists, skipping"
else
    gcloud iam workload-identity-pools providers create-oidc "$WIF_PROVIDER" \
        --location=global \
        --workload-identity-pool="$WIF_POOL" \
        --display-name="GitHub OIDC" \
        --issuer-uri="https://token.actions.githubusercontent.com" \
        --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref" \
        --attribute-condition="assertion.repository == '${GITHUB_REPO}'" \
        --project="$PROJECT_ID"
fi

PROVIDER_NAME=$(gcloud iam workload-identity-pools providers describe "$WIF_PROVIDER" \
    --location=global --workload-identity-pool="$WIF_POOL" \
    --project="$PROJECT_ID" --format='value(name)')

bold "7. Allowing the GitHub repo to impersonate the SA"
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
    --role=roles/iam.workloadIdentityUser \
    --member="principalSet://iam.googleapis.com/${POOL_NAME}/attribute.repository/${GITHUB_REPO}" \
    --project="$PROJECT_ID" \
    --condition=None \
    --quiet >/dev/null

echo
bold "Done. Add these as GitHub repository secrets:"
echo
echo "  GCP_PROJECT_ID                 = $PROJECT_ID"
echo "  GCP_WORKLOAD_IDENTITY_PROVIDER = $PROVIDER_NAME"
echo "  GCP_SERVICE_ACCOUNT_EMAIL      = $SA_EMAIL"
echo
bold "Then create the Cloud Run service for the first time (deploy expects it to exist):"
echo
echo "  gcloud run deploy $SERVICE_NAME \\"
echo "      --image=gcr.io/cloudrun/hello \\"
echo "      --region=$REGION --project=$PROJECT_ID \\"
echo "      --platform=managed --allow-unauthenticated --port=8080"
echo
bold "Then map the custom domain (see deploy/README.md for the Cloudflare CNAME):"
echo "  gcloud beta run domain-mappings create \\"
echo "      --service=$SERVICE_NAME \\"
echo "      --domain=python.ristkari.dev \\"
echo "      --region=$REGION --project=$PROJECT_ID"
```

- [ ] **Step 2: Make it executable and verify it parses**

```bash
chmod +x deploy/setup.sh
bash -n deploy/setup.sh && echo "syntax ok"
```
Expected: `syntax ok`.

- [ ] **Step 3: Commit**

```bash
git add deploy/setup.sh
git commit -m "build: add idempotent GCP bootstrap script for deploy"
```

---

## Task 11: Add the deploy README

**Files:**
- Create: `deploy/README.md`

- [ ] **Step 1: Create `deploy/README.md`**

````markdown
# Deploying python-training slides

The slides site is built into a Docker image, pushed to Google Artifact
Registry, and served by Cloud Run. A push to `main` triggers
`.github/workflows/deploy.yml` which does the build → push → deploy.

The custom domain `https://python.ristkari.dev/` points at the Cloud Run
service via a Cloudflare CNAME (DNS-only).

This file documents the **one-time setup** you do once per project, not what
runs on every push.

## Prerequisites

- `gcloud` CLI authenticated as an account with Owner (or sufficient roles) on
  the `ristkari-dev` project.
- `gh` CLI authenticated against `ristkari-dev/python-training` for setting
  repo secrets (or set them in the GitHub UI).
- Cloudflare access for the `ristkari.dev` zone.

## Step 1 — bootstrap GCP

```bash
./deploy/setup.sh
```

Idempotent / re-runnable. It enables the required APIs, creates Artifact
Registry repo `python-training` in `europe-north1`, creates service account
`github-deploy-python@ristkari-dev.iam.gserviceaccount.com` with
`artifactregistry.writer` + `run.admin` + `iam.serviceAccountUser`, creates the
shared `github-actions` WIF pool (if missing) and a repo-scoped OIDC provider
`github-python-training`, binds the repo to impersonate the SA, and prints the
three values to set as GitHub repo secrets.

## Step 2 — set GitHub repo secrets

```bash
gh secret set GCP_PROJECT_ID                 -b "ristkari-dev"
gh secret set GCP_WORKLOAD_IDENTITY_PROVIDER -b "<value-from-setup-output>"
gh secret set GCP_SERVICE_ACCOUNT_EMAIL      -b "github-deploy-python@ristkari-dev.iam.gserviceaccount.com"
```

Or set them in the GitHub UI: **Settings → Secrets and variables → Actions**.

## Step 3 — first-time service materialisation

The deploy workflow uses `gcloud run services replace deploy/cloudrun.yaml`,
which works only if the service already exists. Create it once with a
placeholder image:

```bash
gcloud run deploy python-training-slides \
    --image=gcr.io/cloudrun/hello \
    --region=europe-north1 \
    --project=ristkari-dev \
    --platform=managed \
    --allow-unauthenticated \
    --port=8080
```

The first push to `main` then replaces it with the real image.

## Step 4 — map the custom domain

```bash
gcloud beta run domain-mappings create \
    --service=python-training-slides \
    --domain=python.ristkari.dev \
    --region=europe-north1 \
    --project=ristkari-dev
```

Output includes a CNAME target like `ghs.googlehosted.com.`.

## Step 5 — Cloudflare DNS

Add a CNAME in the Cloudflare dashboard for `ristkari.dev`:

| Type  | Name   | Target                 | Proxy status              |
|-------|--------|------------------------|---------------------------|
| CNAME | python | `ghs.googlehosted.com` | **DNS only** (gray cloud) |

Leave it gray — Cloudflare proxying (orange cloud) breaks Cloud Run's managed
TLS at the mapped hostname.

Verify:

```bash
dig python.ristkari.dev CNAME +short
gcloud beta run domain-mappings describe \
    --domain=python.ristkari.dev \
    --region=europe-north1 \
    --project=ristkari-dev
```

`READY=True` and HTTPS serving follow once Google provisions the managed
certificate (a few minutes after DNS propagates).

## Verifying a deploy

```bash
gh run watch                                   # watch the deploy workflow
curl -sS -I https://python.ristkari.dev/       # expect HTTP/2 200, text/html
```

Service URL without the custom domain:

```bash
gcloud run services describe python-training-slides \
    --region=europe-north1 --project=ristkari-dev \
    --format='value(status.url)'
```

## Rolling back

```bash
gcloud run revisions list --service=python-training-slides \
    --region=europe-north1 --project=ristkari-dev
gcloud run services update-traffic python-training-slides \
    --to-revisions=python-training-slides-<previous-revision>=100 \
    --region=europe-north1 --project=ristkari-dev
```
````

- [ ] **Step 2: Commit**

```bash
git add deploy/README.md
git commit -m "docs: add deploy/README with one-time GCP + Cloudflare setup"
```

---

## Task 12: Add the CI and deploy GitHub Actions workflows

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: Create `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Sync workspace
        run: uv sync --frozen --all-packages

      - name: Lint (ruff)
        run: uv run ruff check .

      - name: Format check (ruff)
        run: uv run ruff format --check .

      - name: Type-check (mypy)
        run: uv run mypy tools/new_lesson/src tools/slides_dev/src tools/build_index/src

      - name: Tool tests
        run: uv run pytest tools

      - name: Build static slides site
        run: make slides-build

      - name: Verify dist contents
        run: |
          test -f dist/index.html
          grep -q "Python Training" dist/index.html
```

> **Why no lesson-test step yet:** `lessons/` is empty in Plan B. When Phase 1 adds lessons, a `make test` / per-lesson step is added here (and the `make test` multi-lesson collision noted in PR #1 must be fixed first).

- [ ] **Step 2: Create `.github/workflows/deploy.yml`**

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  id-token: write

env:
  REGION: europe-north1
  AR_REPO: python-training
  IMAGE_NAME: slides
  SERVICE_NAME: python-training-slides

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Verify required secrets are set
        env:
          PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
          WIP: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          SA: ${{ secrets.GCP_SERVICE_ACCOUNT_EMAIL }}
        run: |
          missing=()
          [ -z "$PROJECT_ID" ] && missing+=("GCP_PROJECT_ID")
          [ -z "$WIP" ]        && missing+=("GCP_WORKLOAD_IDENTITY_PROVIDER")
          [ -z "$SA" ]         && missing+=("GCP_SERVICE_ACCOUNT_EMAIL")
          if [ ${#missing[@]} -ne 0 ]; then
            echo "::error::Missing required secrets: ${missing[*]}"
            echo "See deploy/README.md for setup instructions."
            exit 1
          fi

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT_EMAIL }}

      - uses: google-github-actions/setup-gcloud@v2

      - name: Configure Docker for Artifact Registry
        env:
          REGION: ${{ env.REGION }}
        run: gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

      - name: Build and push image
        id: build
        env:
          REGION: ${{ env.REGION }}
          AR_REPO: ${{ env.AR_REPO }}
          IMAGE_NAME: ${{ env.IMAGE_NAME }}
          PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
          SHA: ${{ github.sha }}
        run: |
          IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/${IMAGE_NAME}:${SHA}"
          docker build -t "$IMAGE" -f deploy/Dockerfile .
          docker push "$IMAGE"
          echo "image=$IMAGE" >> "$GITHUB_OUTPUT"

      - name: Render Cloud Run spec
        env:
          IMAGE: ${{ steps.build.outputs.image }}
        run: |
          sed "s|__IMAGE__|${IMAGE}|" deploy/cloudrun.yaml > /tmp/cloudrun.rendered.yaml

      - name: Deploy to Cloud Run
        env:
          REGION: ${{ env.REGION }}
          PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
        run: |
          gcloud run services replace /tmp/cloudrun.rendered.yaml \
              --region="$REGION" \
              --project="$PROJECT_ID"

      - name: Allow public access (idempotent)
        env:
          SERVICE_NAME: ${{ env.SERVICE_NAME }}
          REGION: ${{ env.REGION }}
          PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
        run: |
          gcloud run services add-iam-policy-binding "$SERVICE_NAME" \
              --region="$REGION" \
              --project="$PROJECT_ID" \
              --member=allUsers \
              --role=roles/run.invoker

      - name: Print service URL
        env:
          SERVICE_NAME: ${{ env.SERVICE_NAME }}
          REGION: ${{ env.REGION }}
          PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
        run: |
          gcloud run services describe "$SERVICE_NAME" \
              --region="$REGION" \
              --project="$PROJECT_ID" \
              --format='value(status.url)'
```

- [ ] **Step 3: Validate YAML parses**

Run:
```bash
uv run python -c "import yaml,sys; [yaml.safe_load(open(p)) for p in ['.github/workflows/ci.yml','.github/workflows/deploy.yml']]; print('yaml ok')" 2>/dev/null || python3 -c "import yaml; [yaml.safe_load(open(p)) for p in ['.github/workflows/ci.yml','.github/workflows/deploy.yml']]; print('yaml ok')"
```
Expected: `yaml ok`. (If `pyyaml` isn't available in either interpreter, fall back to: `for f in .github/workflows/*.yml; do grep -q '^name:' "$f" && echo "$f has name"; done` and confirm both files have a top-level `name:`.)

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml .github/workflows/deploy.yml
git commit -m "ci: add CI (lint/type/test/build) and Cloud Run deploy workflows"
```

---

## Task 13: Local Docker smoke test + final verification

This task requires Docker running locally. If Docker is unavailable, mark the Docker sub-steps BLOCKED and report — do not fake the result.

- [ ] **Step 1: Build the deploy image**

Run: `docker build -t python-training-slides:local -f deploy/Dockerfile .`
Expected: build succeeds. The builder stage runs `uv sync` + `build_index`; the runtime stage is `nginx-unprivileged`.

- [ ] **Step 2: Run the container and curl it**

```bash
docker run --rm -d -p 8080:8080 -e PORT=8080 --name pt-slides-smoke python-training-slides:local
sleep 2
curl -s -o /dev/null -w "root=%{http_code}\n" http://127.0.0.1:8080/
curl -s http://127.0.0.1:8080/ | grep -o "<title>[^<]*</title>"
curl -s -o /dev/null -w "revealcss=%{http_code}\n" http://127.0.0.1:8080/shared/reveal/dist/reveal.css
curl -s -o /dev/null -w "notfound=%{http_code}\n" http://127.0.0.1:8080/nope.txt
docker stop pt-slides-smoke
```
Expected: `root=200`, `<title>Python Training</title>`, `revealcss=200`, `notfound=404`.

- [ ] **Step 3: Full local quality bar**

```bash
make lint
make typecheck
uv run pytest tools
make slides-build && test -f dist/index.html && grep -q "Python Training" dist/index.html && echo "build ok"
rm -rf dist
```
Expected: lint clean, typecheck `Success`, all tool tests pass (28 from Plan A + 20 new from build_index = 48), `build ok`.

> The build_index suite adds 7 (catalog) + 13 (builder) = 20 tests, for 48 total across the three tools. Confirm the count.

- [ ] **Step 4: Confirm no stray artifacts**

```bash
git status --porcelain
```
Expected: clean (no `dist/`, no `*.pyc`, no container leftovers tracked). `dist/` must be gitignored.

- [ ] **Step 5: Final commit (only if anything needs tidying)**

If `git status` shows changes, investigate and commit intentionally. If clean, skip.

---

## Notes for execution

- **No `gcloud`, no `git push`, no secrets** are touched by this plan. The deploy files are written and locally validated; activating the pipeline is the owner's manual one-time `deploy/setup.sh` + secret-setting + DNS, documented in `deploy/README.md`.
- The deploy workflow will run on the first push to `main` after merge, but it will fail fast at the "Verify required secrets" step until the owner completes the one-time setup — that's the intended, safe default.
- After this plan, `lessons/` is still empty; the landing page shows all 28 lessons as faded placeholders, which is the correct pre-content state.
