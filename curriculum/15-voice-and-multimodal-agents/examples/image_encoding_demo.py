"""Run: uv run python curriculum/15-voice-and-multimodal-agents/examples/image_encoding_demo.py

Shows how a Message carries an image (base64-encoded, media type by
extension) and how AnthropicProvider's wire format looks once built. No API
key needed -- this only exercises encoding and message construction, not a
real model call. See lessons/01-vision-inputs.md.
"""

from __future__ import annotations

import base64
import json
import struct
import tempfile
import zlib
from pathlib import Path

from shared.llm import ImageContent, Message, Role
from shared.llm.providers.anthropic_provider import AnthropicProvider


def _write_tiny_png(path: Path) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

    width = height = 2
    raw = bytearray()
    for _ in range(height):
        raw.append(0)
        for _ in range(width):
            raw.extend((10, 20, 30))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw)))
        + chunk(b"IEND", b"")
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        image_path = Path(tmp) / "tiny.png"
        _write_tiny_png(image_path)

        data_base64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
        image = ImageContent(media_type="image/png", data_base64=data_base64)
        message = Message(role=Role.USER, content="What color is this?", images=[image])

        print(f"Image bytes: {len(image_path.read_bytes())}")
        print(f"Base64 length: {len(image.data_base64)}")

        _, wire = AnthropicProvider._to_wire([message])
        print("Anthropic wire format:")
        print(json.dumps(wire, indent=2)[:300], "...")


if __name__ == "__main__":
    main()
