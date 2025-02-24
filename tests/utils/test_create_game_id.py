import pytest
from ideation_cli import utils

pytestmark = pytest.mark.unit


def test_create_game_id_removes_spaces():
    # A simple string with spaces.
    assert utils.create_game_id("hello world") == "helloworld"
    # Leading, trailing and multiple spaces.
    input_str = "  multiple   spaces  "
    expected = "multiplespaces"
    assert utils.create_game_id(input_str) == expected
