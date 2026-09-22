"""Run: uv run python curriculum/00-programming-prerequisites/examples/http_demo.py

Spins up a tiny local HTTP server (no network access needed) and makes both a
successful and a failing request against it with httpx, showing status-code
handling as covered in lessons/03-http-and-rest.md.
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import httpx


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (stdlib's required method name)
        if self.path == "/status":
            body = json.dumps({"status": "ok"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass  # keep the demo's output quiet


def main() -> None:
    server = HTTPServer(("127.0.0.1", 0), DemoHandler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        ok_response = httpx.get(f"http://127.0.0.1:{port}/status")
        print("GET /status ->", ok_response.status_code, ok_response.json())

        missing_response = httpx.get(f"http://127.0.0.1:{port}/does-not-exist")
        print("GET /does-not-exist ->", missing_response.status_code)
        try:
            missing_response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print("raise_for_status() correctly raised:", exc)
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
