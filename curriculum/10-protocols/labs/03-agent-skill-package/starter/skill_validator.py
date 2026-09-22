"""Lab 10.03: package a tool as an Agent Skill. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/10-protocols/labs/03-agent-skill-package/tests
"""

from __future__ import annotations

import re  # noqa: F401 -- used once you implement parse_skill_frontmatter below
from pathlib import Path

import yaml  # noqa: F401 -- used once you implement parse_skill_frontmatter below


def parse_skill_frontmatter(skill_md_text: str) -> dict:
    """Extract and parse the YAML frontmatter block. Raise ValueError if none found.

    TODO: implement this.
    """
    raise NotImplementedError


def validate_skill_frontmatter(frontmatter: dict) -> list[str]:
    """Return a list of human-readable error strings (empty = valid).

    TODO: implement this. Check for missing "name", missing "description",
    and a "description" shorter than 10 characters.
    """
    raise NotImplementedError


def validate_skill_folder(skill_dir: Path) -> list[str]:
    """Return errors: missing SKILL.md, or frontmatter validation errors.

    TODO: implement this.
    """
    raise NotImplementedError
