import pytest
from ideation_cli import MODEL_CHOICES, IDEATION_TECHNIQUES

pytestmark = pytest.mark.unit


def test_model_choices_entries():
    expected_model_choices = [
        "o1-mini",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
        "o1-preview",
    ]
    # Assert that the MODEL_CHOICES list exactly matches the expected list.
    assert MODEL_CHOICES == expected_model_choices


def test_ideation_techniques_entries():
    expected_ideation_techniques = [
        "Brainstorming",
        "Mind Maps",
        "Round Robin",
        "Opposite Thinking",
        "Cut-Up",
        "Mash-Up",
        "Crazy Eights",
        "SCAMPER",
        "Oblique Strategy",
    ]
    # Assert that the IDEATION_TECHNIQUES list exactly matches the expected list.
    assert IDEATION_TECHNIQUES == expected_ideation_techniques
