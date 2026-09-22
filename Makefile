.PHONY: setup test test-live lint format docs check-links

setup:
	uv sync --all-groups

test:
	uv run pytest

test-live:
	uv run pytest -m live

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

docs:
	uv run python scripts/sync_docs.py
	uv run mkdocs build

docs-serve:
	uv run python scripts/sync_docs.py
	uv run mkdocs serve

check-links:
	uv run python scripts/check_links.py
