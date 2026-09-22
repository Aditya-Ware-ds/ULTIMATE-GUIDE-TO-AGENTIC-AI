VALID_SKILL_MD = """---
name: example
description: A description that is definitely long enough to pass validation.
---

Body text here.
"""

MISSING_NAME = """---
description: A description that is definitely long enough to pass validation.
---

Body text.
"""

MISSING_DESCRIPTION = """---
name: example
---

Body text.
"""

SHORT_DESCRIPTION = """---
name: example
description: too short
---

Body text.
"""

NO_FRONTMATTER = "# Just a heading, no frontmatter at all\n"


def test_parse_skill_frontmatter_valid(skill_validator):
    frontmatter = skill_validator.parse_skill_frontmatter(VALID_SKILL_MD)

    assert frontmatter["name"] == "example"
    assert "description" in frontmatter


def test_parse_skill_frontmatter_raises_without_frontmatter(skill_validator):
    import pytest

    with pytest.raises(ValueError):
        skill_validator.parse_skill_frontmatter(NO_FRONTMATTER)


def test_validate_skill_frontmatter_valid_has_no_errors(skill_validator):
    frontmatter = skill_validator.parse_skill_frontmatter(VALID_SKILL_MD)

    errors = skill_validator.validate_skill_frontmatter(frontmatter)

    assert errors == []


def test_validate_skill_frontmatter_missing_name(skill_validator):
    frontmatter = skill_validator.parse_skill_frontmatter(MISSING_NAME)

    errors = skill_validator.validate_skill_frontmatter(frontmatter)

    assert any("name" in e.lower() for e in errors)


def test_validate_skill_frontmatter_missing_description(skill_validator):
    frontmatter = skill_validator.parse_skill_frontmatter(MISSING_DESCRIPTION)

    errors = skill_validator.validate_skill_frontmatter(frontmatter)

    assert any("description" in e.lower() for e in errors)


def test_validate_skill_frontmatter_short_description(skill_validator):
    frontmatter = skill_validator.parse_skill_frontmatter(SHORT_DESCRIPTION)

    errors = skill_validator.validate_skill_frontmatter(frontmatter)

    assert any("short" in e.lower() for e in errors)


def test_validate_skill_folder_missing_skill_md(skill_validator, tmp_path):
    errors = skill_validator.validate_skill_folder(tmp_path)

    assert len(errors) == 1
    assert "SKILL.md" in errors[0]


def test_validate_skill_folder_with_valid_skill_md(skill_validator, tmp_path):
    (tmp_path / "SKILL.md").write_text(VALID_SKILL_MD)

    errors = skill_validator.validate_skill_folder(tmp_path)

    assert errors == []


def test_hand_written_calculator_skill_is_valid(skill_validator, calculator_skill_dir):
    """The hand-written starter/solution calculator/SKILL.md must itself pass
    validation with zero errors -- this is the lab's real deliverable, not
    just the Python validator code.
    """
    errors = skill_validator.validate_skill_folder(calculator_skill_dir)

    assert errors == [], f"calculator/SKILL.md has validation errors: {errors}"
