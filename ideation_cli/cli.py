"""
cli.py - Command-Line Interface for the Ideation CLI.

This module provides the main entry point for the Ideation CLI, allowing users
to generate game ideas, apply creative ideation techniques, and produce branding
assets. The CLI supports both interactive mode and argument-based execution.

Features:
    - Interactive mode for user-driven idea generation.
    - Automated game idea generation based on predefined strategies.
    - Application of Brian Eno's Oblique Strategies to ideation.
    - Branding asset generation, including names and cover images.
    - JSON output storage for reproducibility.

Functions:
    - cli(): Handles command-line input, processes arguments, and executes
             the necessary game generation workflows.

Dependencies:
    - json
    - os
    - ideation_cli.generator (for branding and idea generation)
    - ideation_cli.strategies (for game prompts and oblique strategies)
    - ideation_cli.utils (for argument parsing, interactive mode, and file handling)

Usage:
    Run the CLI tool directly from the terminal:

    ```bash
    python cli.py --random-game --branding
    ```

    Alternatively, use interactive mode if no arguments are provided:

    ```bash
    python cli.py
    ```

"""

import json
import os

from pydantic_core.core_schema import none_schema

from ideation_cli.generator import (
    generate_metadata,
    generate_name,
    generate_cover,
    generate_ideas,
)
from ideation_cli.strategies import generate_random_game_prompt, apply_oblique_strategy
from ideation_cli.utils import (
    parse_arguments,
    use_interactive_mode,
    save_args_to_json,
    create_game_id,
)


def cli():
    """Command-line interface for ideation techniques."""
    args = parse_arguments()

    if args is None:  # No arguments provided, use interactive mode
        artifact, technique, count, model = use_interactive_mode()
        generate_ideas(artifact, technique.lower().replace(" ", "_"), count, model)
        return

    # Process logic based on flags
    task = args.task
    game_type = args.type
    model = args.model
    count = args.count
    errors = None

    for i in range(count):
        if args.randomize:
            task, game_type = generate_random_game_prompt()

        if args.oblique_strategy:
            task = apply_oblique_strategy(task)

        print(task)

        name = generate_name(task, model).strip()
        game_type = game_type.replace(" ", "")

        game_id = create_game_id(name)
        dir_path = os.path.join(args.path, game_type, game_id)
        os.makedirs(dir_path, exist_ok=True)

        # Generate metadata
        metadata = generate_metadata(task, name, model)
        try:
            metadata_json = json.loads(metadata)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            errors = str(e)
            metadata_json = metadata

        # Generate a cover image
        if args.cover:
            generate_cover(task, name, dir_path)

        # Prepare output dictionary
        output = vars(args).copy()  # Copy to avoid modifying original args
        output.update(
            {
                "task": task,
                "name": name,
                "game_type": game_type if game_type else None,
                "branding_data": metadata_json,
                "errors": errors if errors else None,
            }
        )

        # Save the arguments to a JSON file
        save_args_to_json(output, dir_path)


if __name__ == "__main__":
    cli()
