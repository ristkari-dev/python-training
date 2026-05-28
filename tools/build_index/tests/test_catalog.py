from build_index.catalog import ALL_LESSONS, PHASES


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
