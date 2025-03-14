import json
import os
import pytest

from ideation_cli import generator

pytestmark = pytest.mark.unit


# --- Fake response classes and helper functions for mocking ---


class FakeChoice:
    def __init__(self, content):
        self.message = type("Message", (), {"content": content})


class FakeResponse:
    def __init__(self, content):
        self.choices = [FakeChoice(content)]


class FakeImageResponse:
    def __init__(self, url):
        self.data = [type("Image", (), {"url": url})]


def fake_create_idea(**kwargs):
    return FakeResponse("idea content")


def fake_create_name(**kwargs):
    # Return a response with quotes to test stripping logic.
    return FakeResponse('"game title"')


def fake_create_metadata(**kwargs):
    # Return a JSON response wrapped in markdown formatting.
    json_response = (
        '{"short_description": "short", "detailed_description": "detailed", "tags": []}'
    )
    return FakeResponse(f"```json\n{json_response}\n```")


def fake_create_image_prompt_api(**kwargs):
    # Simulate a call to generate an image prompt via the chat API.
    return FakeResponse("Detailed pixel art prompt")


def fake_generate_image_prompt(*args, **kwargs):
    # Fake replacement for generate_image_prompt in generate_cover.
    return "fake generated prompt"


def fake_generate_image(**kwargs):
    # Return a fake image generation response with a fake URL.
    return FakeImageResponse("http://fakeurl.com/cover.png")


class FakeRequestsResponse:
    def __init__(self, content):
        self.content = content


def fake_requests_get(url):
    return FakeRequestsResponse(b"fake image data")


def fake_validate_model(model):
    # Simply return a "validated" model string.
    return "validated-model"


def fake_get_prompt(artifact, technique):
    return f"prompt for {artifact} and {technique}"


def fake_exception_create(**kwargs):
    raise Exception("API error")


# --- Unit Tests ---


def test_generate_ideas(monkeypatch):
    monkeypatch.setattr(generator, "get_prompt", fake_get_prompt)
    monkeypatch.setattr(
        generator.OPENAI_CLIENT.chat.completions, "create", fake_create_idea
    )

    result = generator.generate_ideas("artifact", "technique", "model")
    assert result == "idea content"


def test_generate_name(monkeypatch):
    monkeypatch.setattr(generator, "validate_model", fake_validate_model)
    monkeypatch.setattr(
        generator.OPENAI_CLIENT.chat.completions, "create", fake_create_name
    )

    result = generator.generate_name("A game about space", "model")
    # The function should strip surrounding quotes from the response.
    assert result == "game title"


def test_generate_metadata(monkeypatch):
    monkeypatch.setattr(generator, "validate_model", fake_validate_model)
    monkeypatch.setattr(
        generator.OPENAI_CLIENT.chat.completions, "create", fake_create_metadata
    )

    result = generator.generate_metadata("a game concept", "GameName", "model")
    # The result should be parsed as JSON and returned as a dict.
    assert isinstance(result, dict)
    assert result["short_description"] == "short"
    assert result["detailed_description"] == "detailed"
    assert result["tags"] == []


def test_generate_image_prompt(monkeypatch):
    # Patch the chat.completions.create call to simulate generating an image prompt.
    monkeypatch.setattr(
        generator.OPENAI_CLIENT.chat.completions, "create", fake_create_image_prompt_api
    )

    result = generator.generate_image_prompt(
        "a game concept", "GameName", model="gpt-4", temperature=0.7
    )
    assert result == "Detailed pixel art prompt"


def test_generate_cover(monkeypatch, tmp_path):
    # Patch generate_image_prompt to use our fake function.
    monkeypatch.setattr(generator, "generate_image_prompt", fake_generate_image_prompt)
    # Patch the image generation and requests.get calls.
    monkeypatch.setattr(generator.OPENAI_CLIENT.images, "generate", fake_generate_image)
    monkeypatch.setattr(generator.requests, "get", fake_requests_get)

    # Use the tmp_path fixture for a temporary directory.
    temp_dir = str(tmp_path)
    result, prompt = generator.generate_cover(
        "a game concept", "GameName", temp_dir, prompt_model="gpt-4", temperature=0.7
    )

    # Expected file path for the cover image.
    expected_path = os.path.join(temp_dir, "cover.png")
    if result is not None:
        assert result == expected_path
    # Verify that the image file was written with the correct content.
    assert os.path.exists(expected_path)
    with open(expected_path, "rb") as f:
        content = f.read()
    assert content == b"fake image data"


def test_generate_name_exception(monkeypatch):
    monkeypatch.setattr(generator, "validate_model", fake_validate_model)
    monkeypatch.setattr(
        generator.OPENAI_CLIENT.chat.completions, "create", fake_exception_create
    )

    with pytest.raises(Exception, match="API error"):
        generator.generate_name("A game about space", "model")


def test_generate_metadata_exception(monkeypatch):
    monkeypatch.setattr(generator, "validate_model", fake_validate_model)
    monkeypatch.setattr(
        generator.OPENAI_CLIENT.chat.completions, "create", fake_exception_create
    )

    with pytest.raises(Exception, match="API error"):
        generator.generate_metadata("a game concept", "GameName", "model")
