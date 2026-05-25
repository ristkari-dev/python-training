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
- Docker (only for `make slides-docker`)

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
