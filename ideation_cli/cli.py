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
from ideation_cli.strategies import generate_random_game_prompt
from ideation_cli.utils import (
    parse_arguments,
    use_interactive_mode,
    save_args_to_json,
    create_game_id,
)


def cli():
    """Command-line interface for ideation techniques."""
    args = parse_arguments()

    # If interactive mode is selected, gather interactive parameters
    if args.interactive:
        interactive_params = use_interactive_mode()  # returns a dict with all options
        # Merge interactive parameters into args by updating the args dict.
        args_dict = vars(args)
        args_dict.update(interactive_params)
        # Convert back to a simple namespace-like object
        args = type("Args", (), args_dict)

    # Process parameters from either mode
    task = args.task
    game_type = args.type
    model = args.model
    count = args.count
    name = args.name

    # If randomize is set, override task and game_type with a random game prompt.
    if args.randomize:
        task, game_type = generate_random_game_prompt(game_type)

    # If no task was provided, warn the user.
    if not task:
        print("No task provided. Exiting.")
        return

    # Generate a name if not provided
    if not name:
        name = generate_name(task, model).strip()
        print(f"Generated name: {name}")

    # Create a unique game ID from the name and current timestamp
    base_game_id = create_game_id(name)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    game_id = f"{base_game_id}_{timestamp}"

    # Create the project directory structure
    # Remove spaces from game_type for directory naming consistency.
    game_dir = game_type.replace(" ", "") if game_type else "default"
    dir_path = os.path.join(args.path, game_dir, game_id)
    os.makedirs(dir_path, exist_ok=True)

    # Generate metadata and try to load it as JSON
    metadata = generate_metadata(task, name, model)
    try:
        metadata_json = json.loads(metadata)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in metadata: {e}")
        metadata_json = metadata

    # Generate cover image if requested
    if args.cover:
        generate_cover(task, name, dir_path)

    # Prepare an output dictionary with all relevant parameters
    output = {
        "randomize": args.randomize,
        "ideation_technique": args.ideation_technique,
        "cover": args.cover,
        "task": task,
        "path": args.path,
        "type": game_type,
        "model": model,
        "count": count,
        "name": name,
        "game_id": game_id,
        "branding_data": metadata_json,
    }

    # Optionally, generate ideas (if this is part of your workflow)
    generate_ideas(task, game_type.lower().replace(" ", "_"), count, model)

    # Save output parameters to JSON for reproducibility
    save_args_to_json(output, dir_path)


if __name__ == "__main__":
    cli()
