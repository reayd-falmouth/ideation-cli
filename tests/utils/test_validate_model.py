import pytest
from ideation_cli import utils

pytestmark = pytest.mark.unit


# For testing, we override MODEL_CHOICES.
@pytest.fixture(autouse=True)
def set_model_choices(monkeypatch):
    monkeypatch.setattr(utils, "MODEL_CHOICES", ["gpt-4", "gpt-3"])


def test_validate_model_valid(capsys):
    # Providing a valid model should return the same value.
    model = utils.validate_model("gpt-4")
    assert model == "gpt-4"
    # Nothing should be printed to stdout.
    captured = capsys.readouterr().out
    assert "Not a valid model" not in captured


def test_validate_model_invalid(capsys):
    # Providing an invalid model should print a notice and return the default.
    model = utils.validate_model("invalid-model")
    captured = capsys.readouterr().out
    assert "Not a valid model" in captured
    # The default is the first element of MODEL_CHOICES.
    assert model == "gpt-4"
