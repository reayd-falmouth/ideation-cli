"""
cli.py - Command-Line Interface for the Ideation CLI.

This module provides the main entry point for the Ideation CLI, allowing users
to generate game ideas, apply creative ideation techniques, and produce branding
assets. The CLI supports both interactive mode and argument-based execution.
"""

import json
import os
from datetime import datetime

from ideation_cli.generator import (
    generate_metadata,
    generate_name,
    generate_cover,
    generate_ideas,
)
from ideation_cli.strategies import (
    generate_random_game_prompt,
    apply_ideation_technique,
)
from ideation_cli.utils import (
    parse_arguments,
    use_interactive_mode,
    save_args_to_json,
    create_game_id,
)


def process_game_iteration(args) -> None:
    """Processes a single game iteration based on the provided arguments."""
    # Determine the task and game type.
    if args.randomize:
        _task, _game_type = generate_random_game_prompt(args.game_type, args.theme)
        print(f"Prompt: {_task}")
    else:
        _task = args.task
        _game_type = args.game_type

    # If no task was provided, skip this iteration.
    if not _task:
        print("No task provided. Skipping iteration.")
        return

    # Apply ideation technique if specified.
    if args.ideation_technique:
        _task, strategy = apply_ideation_technique(_task, args.ideation_technique)
        print(f"New task with ideation technique: {strategy}")

    # Generate a name if none was provided.
    if not args.name:
        _name = generate_name(_task, args.model, args.temperature, args.top_p).strip()
        print(f"Generated name: {_name}")
    else:
        _name = args.name

    # Create a unique game ID using the name and the current timestamp.
    base_game_id = create_game_id(_name)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    game_id = f"{base_game_id}_{timestamp}"
    safe_game_id = game_id.replace("Title:", "").replace('"', "").replace(" ", "_")
    game_dir = _game_type.replace(" ", "") if _game_type else "default"
    dir_path = os.path.join(args.path, game_dir, safe_game_id)
    os.makedirs(dir_path, exist_ok=True)

    # Generate metadata and attempt to parse it as JSON.
    metadata = generate_metadata(_task, _name, args.model)
    if isinstance(metadata, str):
        try:
            metadata_json = json.loads(metadata)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in metadata: {e}")
            metadata_json = metadata
    else:
        metadata_json = metadata

    # Generate a cover image if requested.
    if args.image:
        generate_cover(_task, _name, dir_path)

    # Build the output dictionary and save it.
    output = {
        "randomize": args.randomize,
        "ideation_technique": args.ideation_technique,
        "cover": args.image,
        "task": _task,
        "path": args.path,
        "game_type": _game_type,
        "model": args.model,
        "count": args.count,
        "name": _name,
        "game_id": game_id,
        "branding_data": metadata_json,
    }

    save_args_to_json(output, dir_path)


def cli():
    """Command-line interface for ideation techniques."""
    args = parse_arguments()

    # If interactive mode is selected, gather interactive parameters.
    if args.interactive:
        interactive_params = use_interactive_mode()  # returns a dict with all options
        args_dict = vars(args)
        args_dict.update(interactive_params)
        args = type("Args", (), args_dict)

    for _ in range(args.count):
        process_game_iteration(args)


if __name__ == "__main__":
    cli()
