# Lab 10.03 -- Package a tool as an Agent Skill

**Difficulty:** ★★☆☆☆ · **Time:** ~1 hour

## Task

Package Module 03's calculator tool as a valid Agent Skill (a `calculator/`
folder with a `SKILL.md` file), and write a validator that checks a
`SKILL.md` file against the format's required fields.

No API key needed -- this is file parsing and validation, no LLM calls.

## Files

- `starter/skill_validator.py` -- skeleton with the validator to implement
- `starter/calculator/SKILL.md` -- **you write this file** (not Python code -- see below)
- `solution/skill_validator.py`, `solution/calculator/SKILL.md` -- complete reference
- `tests/` -- tests that exercise both

## Requirements

**Write `starter/calculator/SKILL.md`** (a real Markdown file, not Python) with:

- YAML frontmatter (between `---` lines) containing at least `name:
  calculator` and a `description:` that clearly states *when* to use this
  skill (per Module 03's tool-description lesson -- the same "say when to use
  it" principle applies to skill descriptions).
- A body (after the frontmatter) explaining, in prose, how to evaluate a
  basic arithmetic expression safely (mention the `ast`-based approach from
  Module 03, and that `eval()` must never be used on untrusted input).

**Implement these in `starter/skill_validator.py`:**

- `def parse_skill_frontmatter(skill_md_text: str) -> dict` -- extract and
  parse the YAML frontmatter block. Raise `ValueError` if no frontmatter block
  is found (must start with `---` on the first line).
- `def validate_skill_frontmatter(frontmatter: dict) -> list[str]` -- return a
  list of human-readable error strings for missing `name` or `description`
  fields (empty list means valid). Also flag a `description` shorter than 10
  characters as an error (`"description is too short to be useful"`) -- a
  stand-in check for the "say when to use it" principle, since we can't
  mechanically verify the description is *good*, only that it's not
  obviously a placeholder.
- `def validate_skill_folder(skill_dir: Path) -> list[str]` -- return errors
  found by: checking `SKILL.md` exists in `skill_dir` (error if missing), then
  parsing and validating its frontmatter (propagate those errors too).

## Acceptance criteria

- All tests in `tests/` pass against your `starter/skill_validator.py` **and**
  your hand-written `starter/calculator/SKILL.md` passes its own validator
  with zero errors.
- `validate_skill_folder` on a folder with no `SKILL.md` returns a clear error
  mentioning the missing file, not an unhandled exception.
- `validate_skill_frontmatter` catches a missing `name`, a missing
  `description`, and a too-short `description`, independently (i.e. all
  three problems in one frontmatter block should all be reported).

## Hints

- Reuse the frontmatter-extraction regex from
  `curriculum/10-protocols/examples/skill_frontmatter_demo.py` -- this lab
  extends that example into a real validator with a real skill folder.
- `Path("starter/calculator/SKILL.md").read_text()` reads your hand-written file.

## Running the tests

```bash
uv run pytest curriculum/10-protocols/labs/03-agent-skill-package/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/10-protocols/labs/03-agent-skill-package/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 11 -- Frameworks](../../../11-frameworks/README.md)
