"""
utils.py - Utility functions for the Ideation CLI.

This module provides helper functions used throughout the application,
such as input validation, file handling, string manipulation, and
randomized selections.

Functions:
    - load_json(filepath): Load and return the contents of a JSON file.
    - save_json(filepath, data): Save a dictionary as a JSON file.
    - apply_oblique_strategy(prompt): Modify a prompt using a random Oblique Strategy.
    - validate_model(model): Ensure a model name is valid, defaulting to a predefined model.
    - create_game_id(prompt_name): Generate a game ID by removing spaces from the prompt name.
    - parse_arguments(): Parse command-line arguments for the CLI.

Constants:
    - MODEL_CHOICES: A predefined list of available model options.

Usage:
    Import the required utility functions into your scripts as needed:

    ```python
    from utils import validate_model, apply_oblique_strategy
    ```

"""

import argparse
import os
import sys
from json import dump, load

import questionary

from . import MODEL_CHOICES, IDEATION_TECHNIQUES


def parse_arguments():
    """
    Parses command-line arguments for the Ideation CLI.

    This function sets up argument parsing for various options related to game
    generation, branding, and customization of software prompts.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Ideation CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Flag to enable random game and strategy selection
    parser.add_argument(
        "--randomize",
        action="store_true",
        help="Enable random game and strategy selection.",
    )

    # Ideation technique selection
    parser.add_argument(
        "--ideation-technique",
        type=str,
        choices=IDEATION_TECHNIQUES,
        help="Select an ideation technique from available choices.",
    )

    # Flag to generate cover images, descriptions, and tags for branding
    parser.add_argument(
        "--image",
        action="store_true",
        help="Generate a an image to visualise the idea.",
    )

    # Argument to specify the software prompt
    parser.add_argument(
        "--task",
        type=str,
        help="The prompt that defines the idea to be generated.",
    )

    # Argument to specify the directory where ideas will be saved
    parser.add_argument(
        "--path",
        type=str,
        default="ideas",
        help="Directory where ideas will be saved.",
    )

    # Argument to specify the type of game to create
    parser.add_argument(
        "--game-type",
        type=str,
        help="Type of game to create.",
    )

    # Add model selection argument with predefined choices
    parser.add_argument(
        "--model",
        type=str,
        choices=MODEL_CHOICES,
        default="gpt-4o",
        help="Select an AI model from available choices.",
    )

    # Generate a number of ideas
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="How many ideas to generate.",
    )

    # Generate a name
    parser.add_argument(
        "--name",
        type=str,
        help="The name to use, if not provided a random one will be generated based on the task",
    )

    # Interactive mode flag to trigger interactive prompts.
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Trigger interactive mode to input values via prompts.",
    )

    # Change the temperature
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Controls randomness, higher values increase diversity.",
    )

    # Change the top-p
    parser.add_argument(
        "--top-p",
        type=float,
        default=1.0,
        help="The cumulative probability cutoff for token selection. Lower values mean sampling from a smaller, more top-weighted nucleus.",
    )

    # If no command-line arguments (other than the script name) are given, print help and exit.
    if len(sys.argv) == 1:
        parser.print_help()

    return parser.parse_args()


def create_game_id(prompt_name):
    """
    Generates a game ID by removing spaces from the given prompt name.

    Args:
        prompt_name (str): The name of the prompt used to generate the game ID.

    Returns:
        str: A game ID string with spaces removed.
    """
    # Remove spaces from the prompt name to create a compact game ID
    game_id = prompt_name.replace(" ", "")

    return game_id


def validate_model(model):
    """
    Validates whether the given model is in the list of available model choices.

    If the model is not found in `MODEL_CHOICES`, the function defaults to the
    first available model and notifies the user.

    Args:
        model (str): The model name to validate.

    Returns:
        str: A valid model name (either the original or the default fallback).
    """
    if model not in MODEL_CHOICES:
        # Notify the user and default to the first model in the list
        print(f"Not a valid model, using default: {MODEL_CHOICES[0]}")
        model = MODEL_CHOICES[0]

    return model


def load_json(filepath):
    """Load JSON data from a given file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data as a dictionary.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return load(file)


def use_interactive_mode():
    """
    Runs an interactive prompt to gather user input for generating ideas.

    This function prompts the user for each option available via the command-line:
        - randomize (bool): Enable random game and strategy selection.
        - oblique_strategy (bool): Apply an Oblique Strategy.
        - ideation_technique (str): Choose an ideation technique from predefined choices.
        - cover (bool): Generate a cover image.
        - task (str): The prompt that defines the software to be generated.
        - path (str): Directory where ideas will be saved.
        - type (str): Type of game to create.
        - model (str): Select an AI model from available choices.
        - count (int): How many ideas to generate.
        - name (str): The name to use (if not provided, a random one will be generated based on the task).

    Returns:
        dict: A dictionary containing the interactive input for each option.
    """

    # Boolean flags
    randomize = questionary.confirm("Enable random game and strategy selection?").ask()

    cover = questionary.confirm("Generate a cover image?").ask()

    # Text inputs
    task = questionary.text(
        "Enter the task prompt (defines the software to be generated):"
    ).ask()

    path = questionary.text(
        "Enter the directory where ideas will be saved (default: ideas):",
        default="ideas",
    ).ask()

    game_type = questionary.text("Enter the type of game to create:").ask()

    name = questionary.text("Enter a name to use (leave blank for random):").ask()

    # Choice for ideation technique
    ideation_technique = questionary.select(
        "Choose an ideation technique:",
        choices=IDEATION_TECHNIQUES,
        default="Oblique Strategy",
    ).ask()

    # Choice for AI model
    model = questionary.select(
        "Select an AI model:", choices=MODEL_CHOICES, default="gpt-4o"
    ).ask()

    # Numeric input for count
    count_input = questionary.text(
        "How many ideas should be generated? (Default: 1)"
    ).ask()
    try:
        count = int(count_input)
    except (TypeError, ValueError):
        count = 1

    return {
        "randomize": randomize,
        "ideation_technique": ideation_technique,
        "cover": cover,
        "task": task,
        "path": path,
        "type": game_type,
        "model": model,
        "count": count,
        "name": name,
    }


def save_args_to_json(data, dir_path):
    """Save arguments to a timestamped JSON file, ensuring the directory exists."""
    # Define file path
    json_file = os.path.join(dir_path, "metadata.json")

    # Save data to JSON
    with open(json_file, "w", encoding="utf-8") as file_obj:
        dump(data, file_obj, indent=4)

    # print(f"Saved run output to {json_file}")
