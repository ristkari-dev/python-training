# Python Training Course — Design

**Status:** Approved (brainstorming complete, awaiting implementation plan)
**Date:** 2026-05-25
**Owner:** Aki Ristkari

## Summary

A Python programming course delivered as both a code repository and per-lesson reveal.js slide decks. The arc starts at "programming 101" for software engineering students with no prior production language experience and finishes with async/concurrency, typing, web services, packaging, observability, and deployment, suitable for early-career and experienced developers. Hybrid delivery (live + self-study) over one to two semesters.

The repository structure, slide pipeline, and deployment model intentionally mirror the sibling [go-training](../../../../go-training) course so the two can share authoring conventions and infrastructure patterns. Python-specific differences are called out throughout.

## Audience and delivery

- **Audience:** Software engineering students at the start, early-career and experienced engineers by the end. The same arc serves both, with optional "going further" material per lesson for stronger students.
- **Delivery:** Hybrid. Some lessons live (lectures + live coding), some self-study. Each lesson is sized for ~90 minutes of live time plus self-study work.
- **Length:** 1-2 semesters (~24-28 lessons).
- **Language:** English only.

## Hands-on model

- Per-lesson exercises in a starter repo students clone.
- Each exercise ships **runnable starter code** (function stubs return placeholder values or `raise NotImplementedError`) plus **failing `test_*.py` tests** that act as the spec. Students make the tests pass.
- Solutions ship in the same lesson folder under `solutions/`, committed to `main`. Students can peek if stuck.
- **`pytest` is used from lesson 1** — treated as a "magic test runner" until lesson 4 explains it properly.
- Type hints introduced gradually. **`mypy --strict` is enforced from lesson 9 onward** (the lesson that introduces typing); earlier lessons stay un-typed to keep the cognitive load down.

## Curriculum (28 lessons, four phases)

### Phase 1 — Foundations (lessons 1-8)

1. **Hello, Python** — install via `uv`, `uv run`, `python -m`, scripts vs modules, `print`/`input`. First `pytest` run (magic).
2. **Variables, types, operators** — int/float/str/bool/None, truthiness, f-strings, immutability vs mutability intuition, constants by convention.
3. **Control flow** — `if`/`elif`/`else`, `for` over iterables, `while`, `match` teaser, early returns, comprehensions intro.
4. **Functions & tests demystified** — positional/keyword args, defaults, `*args`/`**kwargs`, return tuples. **`pytest` properly introduced** — `assert`, parametrize, fixtures basics.
5. **Collections — list, tuple, dict, set** — methods, idioms, comprehensions in depth, `enumerate`/`zip`, when to pick which.
6. **Classes & dataclasses** — `__init__`, methods, `@dataclass`, instance vs class vs static, simple inheritance, dunder basics (`__repr__`, `__eq__`).
7. **Modules, packages, imports** — files vs modules, `__init__.py`, absolute vs relative imports, the import system mental model, stdlib tour.
8. **Phase 1 capstone — expense tracker CLI** — multiple modules, `argparse`, reading/writing files, using a provided package as a black-box dependency.

### Phase 2 — Idiomatic Python (lessons 9-15)

9. **Type hints & mypy** — `int`, `list[int]`, `Optional`, `Union` (`|`), `TypedDict`, generics intro. **`mypy --strict` from here on.**
10. **Protocols, ABCs, duck typing** — `Protocol`, `abc.ABC`, when to use which, structural vs nominal typing.
11. **Errors & exceptions** — `try`/`except`/`else`/`finally`, exception hierarchy, custom exceptions, EAFP vs LBYL, `raise from`.
12. **Iterators, generators, comprehensions** — iterator protocol, `yield`, generator expressions, `itertools` essentials.
13. **Decorators & context managers** — `@decorator`, `functools.wraps`, `with`, `contextlib`, writing your own.
14. **Files, JSON, paths, dates** — `pathlib`, `json`, `csv`, `datetime`, `zoneinfo`, common encoding gotchas.
15. **Project structure, packaging, testing patterns** — `src/` layout, `pyproject.toml`, console scripts, pytest fixtures/conftest, parametrize, golden files.

### Phase 3 — Async, Concurrency & Tooling (lessons 16-21)

16. **Concurrency overview & threads** — GIL explained honestly, `threading` for I/O, when not to use it.
17. **Multiprocessing & `concurrent.futures`** — pools, `map`, when CPU-bound work warrants it.
18. **`asyncio` basics** — `async`/`await`, event loop, `asyncio.run`, the colored-functions reality.
19. **Async patterns** — `gather`, `TaskGroup`, cancellation, timeouts, `asyncio.Queue`, structured concurrency.
20. **HTTP clients & resilience** — `httpx` async, timeouts, retries (`tenacity`), backoff, structured logging (`logging` stdlib).
21. **Profiling, benchmarking, debugging** — `cProfile`, `pyinstrument`, `memray` intro, `pdb`, `pytest --benchmark`.

### Phase 4 — Production & Services (lessons 22-28)

22. **FastAPI fundamentals** — routing, request/response models with Pydantic, dependency injection, middleware.
23. **FastAPI testing & data validation** — `TestClient`, async tests, Pydantic v2 deeply, error responses.
24. **Databases with SQLAlchemy 2** — engines, sessions, declarative models, migrations with Alembic.
25. **Configuration, secrets, settings** — `pydantic-settings`, env vars, 12-factor, secrets handling, graceful shutdown.
26. **Build, package, containerize** — `uv build`, wheels, multi-stage Dockerfile, distroless/slim images, image size discipline.
27. **Observability** — structured logs, OpenTelemetry traces, Prometheus metrics, health checks, readiness vs liveness.
28. **Distributed patterns & wrap-up** — message queues (concept + one example), idempotency, deployment to Cloud Run-like runtime, course capstone.

### Cross-cutting threads

- **Testing** — `pytest` from lesson 1; testing patterns deepen each phase.
- **Tooling** — `uv` from lesson 1; `ruff format` + `ruff check` from lesson 2; `mypy --strict` from lesson 9; CI runs all three from the start.
- **Typing** — gradual: no hints required in lessons 1-8, hints required from lesson 9 onward. `mypy` `[[tool.mypy.overrides]]` scopes enforcement so earlier lessons stay opt-in.
- **"Going further"** — every lesson README has a section with optional advanced exercises, stdlib reading, and external links for stronger students.

## Repository layout

```
python-training/
├── README.md
├── pyproject.toml              # uv workspace root, ruff + mypy + pytest config
├── uv.lock
├── Makefile
├── .python-version             # pinned Python (e.g., 3.13)
├── .editorconfig
├── .gitignore
│
├── lessons/
│   ├── 01-hello/
│   │   ├── pyproject.toml      # workspace member, per-lesson deps if any
│   │   ├── README.md           # self-study notes + "going further"
│   │   ├── slides/
│   │   │   ├── index.html
│   │   │   ├── slides.md
│   │   │   └── assets/
│   │   ├── exercises/
│   │   │   ├── __init__.py
│   │   │   ├── hello.py
│   │   │   └── test_hello.py
│   │   └── solutions/
│   │       ├── __init__.py
│   │       ├── hello.py
│   │       └── test_hello.py
│   ├── 02-variables/
│   ├── ...
│   └── 28-distributed/
│
├── shared/
│   └── reveal/                 # vendored reveal.js + theme + plugins (pinned)
│       ├── dist/
│       ├── plugin/
│       └── theme/
│
├── deploy/
│   ├── Dockerfile              # two-stage: builder + nginx-unprivileged
│   ├── nginx.conf
│   ├── cloudrun.yaml
│   └── README.md               # one-time GCP setup
│
├── tools/
│   ├── build_index/            # Python: generates dist/index.html + copies decks
│   ├── slides_dev/             # Python: local static server for one deck
│   └── new_lesson/             # Python: scaffolds a new lesson from template
│
├── docs/
│   └── superpowers/specs/      # design docs
│
└── .github/
    └── workflows/
        ├── ci.yml
        └── deploy.yml
```

### Workspace strategy

- Root `pyproject.toml` declares `[tool.uv.workspace] members = ["lessons/*", "tools/*"]`. One shared `.venv` at the root.
- Each lesson is a workspace member with its own `pyproject.toml`. Per-lesson dependencies (e.g., `httpx`, `fastapi`, `sqlalchemy`) declared there, not at the root.
- No cross-lesson imports — each lesson is self-contained, so renumbering or rewriting a lesson never breaks another. Enforced by `ruff` (TID rules) plus convention.
- `uv sync` from the root sets up everything in one shot.
- `pytest lessons/*/solutions` from the root verifies every reference solution passes; this is what CI runs to catch broken specs or solution drift.

## Anatomy of a lesson

Every `lessons/NN-name/` folder contains four parts.

### `README.md`

1. **Learning goals** — 3-5 bullets.
2. **Prereqs** — links to earlier lessons.
3. **Concepts** — 1-3 paragraphs of prose mirroring the deck narrative for self-study.
4. **Exercise brief** — what to build, what `pytest` should show when done.
5. **How to run** — `uv run pytest lessons/NN-name/exercises` (and `uv run python -m exercises.<file>` when applicable).
6. **Going further** — optional advanced material.

### `slides/`

- `index.html` — minimal reveal.js bootstrap referencing `../../shared/reveal/`, configures the markdown plugin, points at `slides.md`.
- `slides.md` — markdown content with `---` horizontal separators and `--` vertical separators (used sparingly). Code in fenced `python` blocks. Speaker notes via `Note:` blocks. HTML escape hatches for layout, fragments, and two-column slides.
- `assets/` — diagrams (SVG preferred), images.

### `exercises/`

- One or more `.py` files with **runnable but incomplete** code: function signatures present, bodies `raise NotImplementedError` or return placeholder values.
- One or more `test_*.py` files with **failing tests**. Tests are the spec.
- Imports kept minimal; no third-party deps unless the lesson explicitly introduces one.

### `solutions/`

- Same package shape as `exercises/`, fully implemented.
- Tests are identical to those in `exercises/` so swapping in `solutions/` and re-running `pytest` passes.
- Brief `# why:` comments only where a choice is non-obvious.

### Conventions

- File names lowercase with underscores (Python convention). Test files always `test_*.py`.
- Each lesson is a single Python package; sub-packages only in late lessons.
- Lesson folder names `NN-kebab-case` with two-digit numbering (`01`, `02`, …, `28`) so listings sort naturally. Inside the folder, the two literal package names are `exercises` and `solutions`.
- Type hints required from lesson 9 onward; before that they are allowed but not enforced.

## Slide deck workflow

### Authoring

- Markdown with HTML escape hatches.
- Code-heavy slides limit to ~15 visible lines; longer examples split across slides with `[highlight]` annotations to focus attention.
- First slide of every deck: lesson number, title, one-line learning goal.
- Last slide: a "what's next" pointer to the next lesson.
- Diagrams as SVG; never images of code.

### Shared assets

- `shared/reveal/` holds a pinned, vendored reveal.js — no CDN.
- `shared/reveal/theme/python-training.css` is a custom theme tuned for code-heavy decks: monospace at readable size, Python blue/yellow accent palette, generous code-block padding, no distracting transitions.
- Default plugins: `markdown`, `highlight`, `notes`, `search`. Anything else is a per-deck escape hatch.

### Per-deck `index.html`

- Identical scaffolding across decks. Loads `../../shared/reveal/dist/reveal.css`, the theme CSS, and a single `<section data-markdown="slides.md" data-separator="^---$" data-separator-vertical="^--$">`.
- `<head>` sets the deck title from the lesson name.
- Generated by `make new-lesson` so authors don't copy-paste.

### Local development

- `make slides-dev LESSON=NN-name` starts a local static server (`uv run python -m tools.slides_dev`) on `localhost:8000` serving the requested lesson.
- A server is needed because reveal.js's markdown plugin uses `fetch`, which doesn't work over `file://`.
- Live reload is optional — drop it if it adds complexity.

### Build for deployment

- `make slides-build` runs `tools/build_index/`, which:
  1. Walks `lessons/*/slides/`.
  2. Generates `dist/index.html` listing every lesson with title and link.
  3. Copies each `slides/` directory and the shared `reveal/` assets into `dist/`, preserving the `lessons/NN/slides/` URL shape.
- Output is fully static. **No npm, no Node — Python stdlib + vendored reveal.js is the entire toolchain.**

## Deployment workflow (Docker + Cloud Run)

### Container image

`deploy/Dockerfile` is two stages:

1. **Build stage** — `python:3.13-slim` (or matching `.python-version`). Installs `uv` via the official installer, runs `uv sync --frozen`, then `make slides-build` to produce the static `dist/`.
2. **Runtime stage** — `nginxinc/nginx-unprivileged:alpine` (Cloud Run requires non-root). Copies `dist/` into `/usr/share/nginx/html/`. Uses `deploy/nginx.conf` which:
   - Listens on `$PORT` (Cloud Run injects this; default `8080`).
   - Serves static files with `Cache-Control: public, max-age=3600` for assets and `no-cache` for HTML.
   - Returns `404` for unknown paths (no SPA fallback).

The runtime image contains no Python — only nginx + static files. Smallest possible attack surface.

### Cloud Run service

- One service (`python-training-slides`) in a single region.
- Public ingress, unauthenticated.
- Min instances `0`, max `1-2`. 256 MiB / 1 vCPU.
- `cloudrun.yaml` (Knative-style service definition) checked in for reproducibility.

### CI/CD

Two GitHub Actions workflows under `.github/workflows/`:

**`ci.yml`** (push/PR):

- Install `uv`, `uv sync --frozen`.
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy lessons/*/solutions` (lesson 9+ paths, scoped via `[[tool.mypy.overrides]]`).
- `uv run pytest lessons/*/solutions` — verifies every reference solution passes.
- `uv run pytest lessons/*/exercises || true` — runs exercise tests, expected to fail; logged for visibility but does not break the build.
- `make slides-build` — verifies the static site builds cleanly.

**`deploy.yml`** (push to `main`):

- Builds the Docker image.
- Authenticates to GCP via Workload Identity Federation (no long-lived service account keys).
- Pushes the image to Artifact Registry.
- Deploys to Cloud Run using `cloudrun.yaml`.

### One-time setup (documented in `deploy/README.md`)

- GCP project + Artifact Registry repo + Cloud Run service.
- WIF pool + GitHub provider mapped to this repo.
- GitHub repo secrets: `GCP_PROJECT_ID`, `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT_EMAIL`. No JSON keys.

### Local parity

- `make slides-docker` builds the same image locally and runs it on `localhost:8080`.

## Tooling and scaffolding

### Makefile

The single canonical entry point. Self-documenting via `make help`:

| Target | What it does |
|---|---|
| `make help` | Lists all targets |
| `make sync` | `uv sync` — install/refresh the workspace venv |
| `make test` | `uv run pytest lessons/*/solutions` — solution tests only |
| `make test-exercises` | `uv run pytest lessons/*/exercises` — fails by design (the spec) |
| `make test-lesson LESSON=NN-name` | Both exercises and solutions for one lesson |
| `make lint` | `uv run ruff check .` |
| `make fmt` | `uv run ruff format .` + `uv run ruff check --fix .` |
| `make typecheck` | `uv run mypy lessons/*/solutions` (lesson 9+ paths) |
| `make slides-dev LESSON=NN-name` | Local server for one deck |
| `make slides-build` | Builds the full static `dist/` |
| `make slides-docker` | Builds and runs the deploy image locally on `:8080` |
| `make new-lesson NAME=NN-name` | Scaffolds a new lesson |

### Lesson scaffolder

`tools/new_lesson/` (a Python program):

- Refuses to overwrite an existing folder.
- Copies a `tools/new_lesson/template/` tree (`pyproject.toml`, `README.md`, `slides/index.html`, `slides/slides.md`, `exercises/{__init__.py, main.py, test_main.py}`, `solutions/{__init__.py, main.py, test_main.py}`).
- Substitutes the lesson name and number where templated.

### Linting and typing

- `ruff` configured in the root `pyproject.toml` under `[tool.ruff]` — a conservative ruleset: `E`, `W`, `F`, `I`, `UP`, `B`, `SIM`, `TID`. No nitpicky rules that fight with teaching examples (line length 100, no docstring rules).
- `ruff format` is the only formatter; `black` is not used.
- `mypy` configured under `[tool.mypy]` — `strict = true`, scoped via per-lesson `[[tool.mypy.overrides]]` so only lesson 9+ paths are enforced. Earlier lessons stay opt-in.
- `.editorconfig` for whitespace consistency.

### Versioning and dependencies

- Python version pinned in `.python-version` and matched in CI + Dockerfile. `uv` reads `.python-version` automatically.
- Reveal.js vendored at a pinned version under `shared/reveal/`. Upgrades are explicit, reviewable commits.
- Third-party Python deps avoided in early/middle lessons. Introduced deliberately and only when a lesson teaches them (e.g., `httpx` in lesson 20, `fastapi` in lesson 22, `sqlalchemy` in lesson 24).
- `uv.lock` committed for reproducibility.

### Documentation in the repo

- Top-level `README.md` — what the course is, prerequisites, install `uv` + clone + run first lesson.
- `CONTRIBUTING.md` — for adding lessons: the four-file convention, `make new-lesson`, slide style.
- `deploy/README.md` — one-time GCP setup.

## Non-goals

- **No npm / no Node toolchain.** Slides build with Python stdlib + vendored static reveal.js.
- **No data-science / ML wedge.** Course is backend-shaped; numpy, pandas, notebooks, and scikit-learn are out of scope.
- **No Django, no Flask.** FastAPI is the only web framework taught.
- **No Kubernetes.** Lesson 26 covers containers; deployment story stops at Cloud Run-style managed runtimes.
- **No parallel "experienced developer" deck per lesson.** Stronger students are served by per-lesson "Going further" sections.
- **No auto-grading service.** Tests in `exercises/` are the spec; students self-verify with `pytest`.
- **No video recording / streaming infrastructure.** Course is hybrid — that's a delivery concern, not a repo concern.
- **No alternative package managers.** `uv` is the only supported toolchain entry point; `pip`/`poetry`/`pipenv` instructions are not included.

## Open items deferred to implementation planning

- Exact Python version pin (current stable at implementation time — likely `3.13`).
- Exact reveal.js version pin (current stable at implementation time).
- Exact GCP region for Cloud Run (depends on owner preference).
- Whether to use Terraform for the GCP setup or a one-shot bash script in `deploy/setup.sh` (default: bash script, swappable later).
- Whether `make slides-dev` includes live reload (default: no, add only if friction warrants).
- Whether to reuse the existing GCP project + WIF from `go-training` or stand up a fresh one (default: reuse — same workload, different image and service name).
