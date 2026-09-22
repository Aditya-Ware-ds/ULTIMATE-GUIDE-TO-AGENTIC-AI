"""Fixtures for the MCP public-API server project: loads starter/ or
solution/ (see shared/testing/lab_loader.py) and spins up a tiny local HTTP
server shaped like Open-Meteo's response, so the default offline test suite
never touches the real internet -- the same pattern Module 00's
async-fetch-cli lab uses.
"""

from __future__ import annotations

import json
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent

_FAKE_RESPONSE = {
    "latitude": 48.85,
    "longitude": 2.35,
    "current": {
        "time": "2026-09-22T12:00",
        "temperature_2m": 18.4,
        "wind_speed_10m": 11.2,
    },
}


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        body = json.dumps(_FAKE_RESPONSE).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass


@pytest.fixture
def local_open_meteo(monkeypatch) -> Iterator[str]:
    server = HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}"
    monkeypatch.setenv("OPEN_METEO_BASE_URL", url)
    try:
        yield url
    finally:
        server.shutdown()
        thread.join(timeout=2)


@pytest.fixture
def server_module():
    return load_lab_module(LAB_DIR, "server")
