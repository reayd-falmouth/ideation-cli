import json
import os
import tempfile
from datetime import datetime

import pytest

from ideation_cli.cli import cli, process_game_iteration

pytestmark = pytest.mark.unit


# --- Fake Implementations for Dependencies ---


def fake_generate_random_game_prompt(game_type, theme):
    return ("Random task", "RandomGameType")


def fake_apply_ideation_technique(task, technique):
    return (f"{task} with {technique}", f"{technique} applied")


def fake_generate_name(task, model, temperature, top_p):
    return "Generated Name"


def fake_generate_metadata(task, name, model):
    # Return a JSON string.
    return (
        '{"short_description": "short", "detailed_description": "detailed", "tags": []}'
    )


def fake_generate_cover(task, name, dir_path):
    # Instead of generating an image, create a dummy file.
    image_path = os.path.join(dir_path, "cover.png")
    with open(image_path, "wb") as f:
        f.write(b"dummy image")
    return image_path


def fake_create_game_id(name):
    return "gameid"


def fake_save_args_to_json(output, dir_path):
    # For testing, simply write the JSON to a file for inspection.
    file_path = os.path.join(dir_path, "output.json")
    with open(file_path, "w") as f:
        json.dump(output, f)


class FakeArgs:
    pass


# --- Helper to create a fake args object ---
def make_fake_args(**overrides):
    args = FakeArgs()
    # Default attributes
    args.interactive = False
    args.task = "Test Task"
    args.game_type = "Test Game"  # This will become "TestGame" directory.
    args.model = "test-model"
    args.count = 1
    args.name = None
    args.ideation_technique = None
    args.temperature = 1.0
    args.top_p = 1.0
    args.theme = "Test Theme"
    args.path = tempfile.gettempdir()
    args.image = False
    args.randomize = False
    for key, value in overrides.items():
        setattr(args, key, value)
    return args


# --- Tests for process_game_iteration ---


def test_process_game_iteration_normal(monkeypatch):
    # Patch dependencies for a normal flow.
    monkeypatch.setattr(
        "ideation_cli.cli.generate_random_game_prompt", fake_generate_random_game_prompt
    )
    monkeypatch.setattr(
        "ideation_cli.cli.apply_ideation_technique", fake_apply_ideation_technique
    )
    monkeypatch.setattr("ideation_cli.cli.generate_name", fake_generate_name)
    monkeypatch.setattr("ideation_cli.cli.generate_metadata", fake_generate_metadata)
    monkeypatch.setattr("ideation_cli.cli.generate_cover", fake_generate_cover)
    monkeypatch.setattr("ideation_cli.cli.create_game_id", fake_create_game_id)
    monkeypatch.setattr("ideation_cli.cli.save_args_to_json", fake_save_args_to_json)

    args = make_fake_args()
    process_game_iteration(args)

    # The directory should be created under args.path/<game_type_no_spaces>/
    game_dir = "TestGame"  # "Test Game" with spaces removed.
    full_game_dir = os.path.join(args.path, game_dir)
    assert os.path.isdir(full_game_dir), "Game type directory not created"

    # Look for a subdirectory that contains "gameid" in its name.
    subdirs = os.listdir(full_game_dir)
    created = [d for d in subdirs if "gameid" in d]
    assert created, "No directory created with gameid"

    # Verify that output.json exists in the created directory.
    dir_path = os.path.join(full_game_dir, created[0])
    output_file = os.path.join(dir_path, "output.json")
    assert os.path.exists(output_file)

    # Read and verify the output content.
    with open(output_file, "r") as f:
        output = json.load(f)
    assert output["task"] == "Test Task"
    assert output["name"] == "Generated Name"
    assert output["model"] == "test-model"

    # Clean up the created directory.
    import shutil

    shutil.rmtree(dir_path)


def test_process_game_iteration_randomize(monkeypatch):
    # Test the randomize branch.
    monkeypatch.setattr(
        "ideation_cli.cli.generate_random_game_prompt", fake_generate_random_game_prompt
    )
    monkeypatch.setattr("ideation_cli.cli.generate_name", fake_generate_name)
    monkeypatch.setattr("ideation_cli.cli.generate_metadata", fake_generate_metadata)
    monkeypatch.setattr("ideation_cli.cli.create_game_id", fake_create_game_id)
    monkeypatch.setattr("ideation_cli.cli.save_args_to_json", fake_save_args_to_json)

    args = make_fake_args(randomize=True)
    process_game_iteration(args)

    # The directory should be created under args.path/<game_type_no_spaces>/
    # For randomize branch, game_type comes from fake_generate_random_game_prompt -> "RandomGameType"
    game_dir = "RandomGameType"
    full_game_dir = os.path.join(args.path, game_dir)
    assert os.path.isdir(
        full_game_dir
    ), "Game type directory not created in randomize branch"

    subdirs = os.listdir(full_game_dir)
    created = [d for d in subdirs if "gameid" in d]
    assert created, "No directory created in randomize branch"

    dir_path = os.path.join(full_game_dir, created[0])
    output_file = os.path.join(dir_path, "output.json")
    with open(output_file, "r") as f:
        output = json.load(f)
    assert output["task"] == "Random task"

    # Clean up the created directory.
    import shutil

    shutil.rmtree(dir_path)


def test_process_game_iteration_no_task(monkeypatch, capsys):
    # If no task is provided, the iteration should skip saving output.
    args = make_fake_args(task="")

    # Patch os.makedirs to capture directory creation.
    mkdir_called = False

    def fake_makedirs(path, exist_ok):
        nonlocal mkdir_called
        mkdir_called = True

    monkeypatch.setattr(os, "makedirs", fake_makedirs)

    # Patch save_args_to_json to raise an error if called.
    def fake_save_args(output, path):
        raise AssertionError(
            "save_args_to_json should not be called when task is empty"
        )

    monkeypatch.setattr("ideation_cli.cli.save_args_to_json", fake_save_args)

    process_game_iteration(args)
    captured = capsys.readouterr().out
    assert "No task provided" in captured
    assert not mkdir_called


# --- Test for the top-level cli() function ---


def fake_parse_arguments():
    class Args:
        pass

    a = Args()
    a.interactive = False
    a.task = "CLI Task"
    a.game_type = "CLI Game"
    a.model = "cli-model"
    a.count = 1
    a.name = None
    a.ideation_technique = None
    a.temperature = 1.0
    a.top_p = 1.0
    a.theme = "CLI Theme"
    a.path = tempfile.gettempdir()
    a.image = False
    a.randomize = False
    return a


def fake_use_interactive_mode():
    return {"task": "Interactive Task", "game_type": "Interactive Game"}


def fake_save_args_to_json_cli(output, dir_path):
    pass


def fake_process_game_iteration(args):
    fake_process_game_iteration.called = True


fake_process_game_iteration.called = False


def test_cli(monkeypatch):
    monkeypatch.setattr("ideation_cli.cli.parse_arguments", fake_parse_arguments)
    monkeypatch.setattr(
        "ideation_cli.cli.use_interactive_mode", fake_use_interactive_mode
    )
    monkeypatch.setattr(
        "ideation_cli.cli.save_args_to_json", fake_save_args_to_json_cli
    )
    monkeypatch.setattr(
        "ideation_cli.cli.process_game_iteration", fake_process_game_iteration
    )

    cli()
    assert (
        fake_process_game_iteration.called
    ), "process_game_iteration was not called in cli()"
