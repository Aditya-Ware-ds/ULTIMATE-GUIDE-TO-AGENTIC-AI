"""Lab 15.01: an agent that answers questions about a bundled image.
Reference solution. See ../README.md.
"""

from __future__ import annotations

import base64
from pathlib import Path

from shared.llm import ImageContent, Message, Role

_MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def load_image(path: Path) -> ImageContent:
    suffix = path.suffix.lower()
    if suffix not in _MEDIA_TYPES:
        raise ValueError(f"Unsupported image type: {suffix!r}")
    data_base64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return ImageContent(media_type=_MEDIA_TYPES[suffix], data_base64=data_base64)


async def ask_about_image(client, image: ImageContent, question: str) -> str:
    response = await client.complete([Message(role=Role.USER, content=question, images=[image])])
    return response.message.content or ""
