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
    # number/dir_name come from the trusted catalog (digits + kebab slug,
    # enforced by catalog tests); title/blurb are free text so they're escaped.
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
