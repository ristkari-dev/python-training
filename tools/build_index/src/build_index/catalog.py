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
    LessonInfo(
        "02", "variables", "Variables, types, operators", "int·float·str·bool·None · f-strings", 1
    ),
    LessonInfo("03", "control-flow", "Control flow", "if·elif · for · while · match", 1),
    LessonInfo("04", "functions", "Functions & tests", "args · *args·**kwargs · pytest", 1),
    LessonInfo("05", "collections", "Collections", "list·tuple·dict·set · comprehensions", 1),
    LessonInfo("06", "classes", "Classes & dataclasses", "__init__ · @dataclass · dunders", 1),
    LessonInfo("07", "modules", "Modules, packages, imports", "__init__.py · imports · stdlib", 1),
    LessonInfo(
        "08", "capstone-cli", "Phase 1 capstone — CLI", "argparse · files · multi-module", 1
    ),
    # Phase 2 — Idiomatic Python
    LessonInfo("09", "type-hints", "Type hints & mypy", "list[int] · Optional · TypedDict", 2),
    LessonInfo(
        "10", "protocols", "Protocols, ABCs, duck typing", "Protocol · abc.ABC · structural", 2
    ),
    LessonInfo("11", "errors", "Errors & exceptions", "try·except · custom · raise from", 2),
    LessonInfo("12", "iterators", "Iterators & generators", "yield · itertools · gen exprs", 2),
    LessonInfo(
        "13", "decorators", "Decorators & context managers", "@decorator · with · contextlib", 2
    ),
    LessonInfo(
        "14",
        "files-json-dates",
        "Files, JSON, paths, dates",
        "pathlib · json · datetime · zoneinfo",
        2,
    ),
    LessonInfo("15", "structure", "Project structure & testing", "src/ · pyproject · fixtures", 2),
    # Phase 3 — Async, Concurrency & Tooling
    LessonInfo("16", "threads", "Concurrency & threads", "GIL · threading · when not to", 3),
    LessonInfo(
        "17", "multiprocessing", "Multiprocessing & futures", "pools · concurrent.futures", 3
    ),
    LessonInfo("18", "asyncio", "asyncio basics", "async·await · event loop", 3),
    LessonInfo("19", "async-patterns", "Async patterns", "gather · TaskGroup · cancellation", 3),
    LessonInfo("20", "http-clients", "HTTP clients & resilience", "httpx · retries · tenacity", 3),
    LessonInfo("21", "profiling", "Profiling & debugging", "cProfile · pyinstrument · pdb", 3),
    # Phase 4 — Production & Services
    LessonInfo("22", "fastapi", "FastAPI fundamentals", "routing · Pydantic · DI · middleware", 4),
    LessonInfo(
        "23", "fastapi-testing", "FastAPI testing & validation", "TestClient · Pydantic v2", 4
    ),
    LessonInfo("24", "databases", "Databases with SQLAlchemy 2", "engine · session · Alembic", 4),
    LessonInfo("25", "config", "Configuration & settings", "pydantic-settings · 12-factor", 4),
    LessonInfo(
        "26", "packaging", "Build, package, containerize", "uv build · wheels · Dockerfile", 4
    ),
    LessonInfo("27", "observability", "Observability", "structured logs · OpenTelemetry", 4),
    LessonInfo(
        "28", "distributed", "Distributed patterns & wrap-up", "queues · idempotency · capstone", 4
    ),
)
