"""Run: uv run python curriculum/10-protocols/examples/skill_frontmatter_demo.py

Parses and validates a SKILL.md file's YAML frontmatter (name + description
required, per the Agent Skills spec). See lessons/03-a2a-and-agent-skills.md.
"""

from __future__ import annotations

import re

import yaml

VALID_SKILL = """---
name: invoice-calculator
description: Calculates invoice totals with tax/discounts. Use for invoice amount or tax questions.
---

# Invoice calculator

To calculate an invoice total: sum the line items, apply any discount
percentage, then apply the tax rate to the discounted subtotal.
"""

INVALID_SKILL = """---
name: invoice-calculator
---

# Invoice calculator (missing a description!)
"""

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_skill_frontmatter(skill_md_text: str) -> dict:
    match = FRONTMATTER_RE.match(skill_md_text)
    if not match:
        raise ValueError("No YAML frontmatter found (must start with '---')")
    return yaml.safe_load(match.group(1))


def validate_skill_frontmatter(frontmatter: dict) -> list[str]:
    errors = []
    if not frontmatter.get("name"):
        errors.append("Missing required field: name")
    if not frontmatter.get("description"):
        errors.append("Missing required field: description")
    return errors


def main() -> None:
    for label, text in [("valid skill", VALID_SKILL), ("invalid skill", INVALID_SKILL)]:
        frontmatter = parse_skill_frontmatter(text)
        errors = validate_skill_frontmatter(frontmatter)
        print(f"{label}: {frontmatter}")
        print(f"  errors: {errors if errors else 'none'}")


if __name__ == "__main__":
    main()
