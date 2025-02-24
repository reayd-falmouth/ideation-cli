import pytest
from ideation_cli import utils

pytestmark = pytest.mark.unit


# Dummy class to simulate questionary responses.
class DummyQuestionary:
    def __init__(self, response):
        self.response = response

    def ask(self):
        return self.response


def test_use_interactive_mode(monkeypatch):
    import questionary

    # Dummy responses for text prompts.
    responses_text = {
        "Enter the task prompt": "Test Task",
        "Enter the directory where ideas will be saved": "test_dir",
        "Enter the type of game to create": "Test Game",
        "Enter a name to use": "TestName",
        "How many ideas should be generated": "3",
    }

    def dummy_text(prompt, **kwargs):
        for key, value in responses_text.items():
            if key in prompt:
                return DummyQuestionary(value)
        # Fallback empty response.
        return DummyQuestionary("")

    monkeypatch.setattr(questionary, "text", dummy_text)

    # Dummy responses for confirm prompts.
    def dummy_confirm(prompt, **kwargs):
        if "random game" in prompt.lower():
            return DummyQuestionary(True)
        elif "cover" in prompt.lower():
            return DummyQuestionary(False)
        # Fallback to False.
        return DummyQuestionary(False)

    monkeypatch.setattr(questionary, "confirm", dummy_confirm)

    # Dummy responses for select prompts.
    responses_select = {
        "Choose an ideation technique": "Brainstorming",
        "Select an AI model": "gpt-4o",
    }

    def dummy_select(prompt, **kwargs):
        for key, value in responses_select.items():
            if key in prompt:
                return DummyQuestionary(value)
        return DummyQuestionary("")

    monkeypatch.setattr(questionary, "select", dummy_select)

    result = utils.use_interactive_mode()

    expected = {
        "randomize": True,
        "ideation_technique": "Brainstorming",
        "cover": False,
        "task": "Test Task",
        "path": "test_dir",
        "type": "Test Game",
        "model": "gpt-4o",
        "count": 3,
        "name": "TestName",
    }

    assert result == expected
