"""Scaffold a new lesson directory from the template tree."""

from __future__ import annotations

import re
import shutil
from importlib.resources import as_file, files
from pathlib import Path
from string import Template

_NAME_RE = re.compile(r"^(\d{2})-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)\Z")


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
            rendered = Template(entry.read_text(encoding="utf-8")).substitute(substitutions)
            (target / entry.stem).write_text(rendered, encoding="utf-8")
        else:
            shutil.copy2(entry, target / entry.name)
