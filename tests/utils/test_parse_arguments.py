import sys
import pytest
from ideation_cli import utils

pytestmark = pytest.mark.unit


def test_parse_arguments_defaults(monkeypatch):
    # Simulate running the script with only the script name (i.e. no additional args)
    monkeypatch.setattr(sys, "argv", ["script_name"])
    args = utils.parse_arguments()

    # Even with no additional args, our parser returns a Namespace with default values.
    assert args.randomize is False
    assert args.ideation_technique is None
    assert args.image is False
    assert args.task is None
    assert args.path == "ideas"
    assert args.game_type is None
    assert args.model == "gpt-4o"
    assert args.count == 1
    assert args.name is None
    assert args.interactive is False


def test_parse_arguments_interactive_flag(monkeypatch):
    # When --interactive is provided, it should be set to True in the namespace.
    monkeypatch.setattr(sys, "argv", ["script_name", "--interactive"])
    args = utils.parse_arguments()
    assert args.interactive is True


def test_parse_arguments_custom(monkeypatch):
    # Provide a complete set of arguments.
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "script_name",
            "--randomize",
            "--ideation-technique",
            "mind_maps",
            "--image",
            "--task",
            "Test Task",
            "--path",
            "/tmp/ideas",
            "--game-type",
            "game",
            "--model",
            "gpt-4o",
            "--count",
            "5",
            "--name",
            "TestName",
        ],
    )
    args = utils.parse_arguments()
    assert args.randomize is True
    assert args.ideation_technique == "mind_maps"
    assert args.image is True
    assert args.task == "Test Task"
    assert args.path == "/tmp/ideas"
    assert args.game_type == "game"
    assert args.model == "gpt-4o"
    assert args.count == 5
    assert args.name == "TestName"
    # Since we did not provide --interactive, it should be False.
    assert args.interactive is False
