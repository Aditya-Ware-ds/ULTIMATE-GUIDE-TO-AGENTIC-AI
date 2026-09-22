"""Lab 15.01: an agent that answers questions about a bundled image.
See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/15-voice-and-multimodal-agents/labs/01-vision-qa-agent/tests
"""

from __future__ import annotations

import base64  # noqa: F401 -- used once you implement load_image below
from pathlib import Path

from shared.llm import ImageContent, Message, Role  # noqa: F401 -- used below

_MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def load_image(path: Path) -> ImageContent:
    """Read `path`, base64-encode its bytes, and return an ImageContent with
    the right media_type looked up from `_MEDIA_TYPES` by file extension
    (case-insensitive). Raise ValueError for an unsupported extension.

    TODO: implement this.
    """
    raise NotImplementedError


async def ask_about_image(client, image: ImageContent, question: str) -> str:
    """Send `question` as a user message with `image` attached (images
    should come before text -- see lessons/01-vision-inputs.md) and return
    the model's text response.

    TODO: implement this.
    """
    raise NotImplementedError
