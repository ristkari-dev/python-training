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
