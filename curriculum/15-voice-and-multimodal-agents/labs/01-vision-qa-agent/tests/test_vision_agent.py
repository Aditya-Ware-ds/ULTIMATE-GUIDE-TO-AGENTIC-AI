import base64

import pytest

from shared.llm import get_client


def test_load_image_produces_valid_base64_png(vision_agent, image_path):
    image = vision_agent.load_image(image_path)

    assert image.media_type == "image/png"
    decoded = base64.b64decode(image.data_base64)
    assert decoded.startswith(b"\x89PNG\r\n\x1a\n")  # PNG file signature


def test_load_image_rejects_unsupported_extension(vision_agent, tmp_path):
    bad_file = tmp_path / "notes.txt"
    bad_file.write_text("not an image")

    with pytest.raises(ValueError):
        vision_agent.load_image(bad_file)


async def test_ask_about_image_sends_image_and_returns_text(vision_agent, client, image_path):
    client.provider.add_text("The background is blue with a red square in the center.")
    image = vision_agent.load_image(image_path)

    result = await vision_agent.ask_about_image(client, image, "What colors are in this image?")

    assert result == "The background is blue with a red square in the center."
    sent_message = client.provider.calls[0]["messages"][0]
    assert sent_message.images == [image]
    assert sent_message.content == "What colors are in this image?"


@pytest.mark.live
async def test_ask_about_image_against_the_real_anthropic_api(vision_agent, image_path):
    """Requires a real ANTHROPIC_API_KEY. Run explicitly with:
    uv run pytest -m live curriculum/15-voice-and-multimodal-agents/labs/01-vision-qa-agent/tests
    """
    client = get_client("anthropic")
    image = vision_agent.load_image(image_path)

    result = await vision_agent.ask_about_image(
        client, image, "What is the dominant background color? Answer in one word."
    )

    assert "blue" in result.lower()
