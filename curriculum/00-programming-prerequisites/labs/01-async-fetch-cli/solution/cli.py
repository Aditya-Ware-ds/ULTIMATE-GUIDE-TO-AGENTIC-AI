"""Lab 00.01: async fetch + JSON CLI -- reference solution. See ../README.md."""

from __future__ import annotations

import asyncio
import sys

import httpx


async def fetch_json(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()


def extract_field(data: dict, field_path: str) -> object:
    value: object = data
    seen: list[str] = []
    for part in field_path.split("."):
        seen.append(part)
        if not isinstance(value, dict) or part not in value:
            raise KeyError(f"field path {'.'.join(seen)!r} not found in response")
        value = value[part]
    return value


async def run(url: str, field_path: str) -> str:
    async with httpx.AsyncClient() as client:
        data = await fetch_json(client, url)
    value = extract_field(data, field_path)
    return str(value)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("Usage: cli.py <url> <field.path>", file=sys.stderr)
        return 1
    url, field_path = args
    try:
        result = asyncio.run(run(url, field_path))
    except (httpx.HTTPStatusError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
