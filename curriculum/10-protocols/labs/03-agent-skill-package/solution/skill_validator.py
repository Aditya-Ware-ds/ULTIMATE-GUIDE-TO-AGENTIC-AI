"""Lab 10.03: package a tool as an Agent Skill -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_skill_frontmatter(skill_md_text: str) -> dict:
    match = _FRONTMATTER_RE.match(skill_md_text)
    if not match:
        raise ValueError("No YAML frontmatter found (file must start with '---')")
    return yaml.safe_load(match.group(1)) or {}


def validate_skill_frontmatter(frontmatter: dict) -> list[str]:
    errors = []
    if not frontmatter.get("name"):
        errors.append("Missing required field: name")
    description = frontmatter.get("description")
    if not description:
        errors.append("Missing required field: description")
    elif len(description) < 10:
        errors.append("description is too short to be useful")
    return errors


def validate_skill_folder(skill_dir: Path) -> list[str]:
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        return [f"Missing required file: {skill_md_path}"]
    frontmatter = parse_skill_frontmatter(skill_md_path.read_text())
    return validate_skill_frontmatter(frontmatter)
