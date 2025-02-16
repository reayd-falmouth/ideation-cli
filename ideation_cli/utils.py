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
from json import dump, load

import questionary

from . import MODEL_CHOICES


def parse_arguments():
    """
    Parses command-line arguments for the Ideation CLI.

    This function sets up argument parsing for various options related to game
    generation, branding, and customization of software prompts.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
        If no arguments are provided, returns None to trigger interactive prompts.
    """
    parser = argparse.ArgumentParser(description="Ideation CLI")

    # Flag to enable random game and strategy selection
    parser.add_argument(
        "--randomize",
        action="store_true",
        help="Enable random game and strategy selection.",
    )

    # Flag to apply one of Brian Eno's Oblique Strategies to development
    parser.add_argument(
        "--oblique-strategy",
        action="store_true",
        help="Apply one of Brian Eno's Oblique Strategies to the development.",
    )

    # Flag to generate cover images, descriptions, and tags for branding
    parser.add_argument(
        "--cover",
        action="store_true",
        help="Generate a cover image",
    )

    # Argument to specify the software prompt
    parser.add_argument(
        "--task",
        type=str,
        default="Develop a basic Gomoku game.",
        help="The prompt that defines the software to be generated.",
    )

    # Argument to specify the directory where ideas are saved
    parser.add_argument(
        "--path",
        type=str,
        default="ideas",
        help="Directory where ideas will be saved.",
    )

    # Argument to specify the type of game to create
    parser.add_argument(
        "--type",
        type=str,
        default="Gomoku",
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

    args = parser.parse_args()

    # If no arguments were provided, return None to trigger interactive questionary prompts
    if not any(vars(args).values()):
        return None

    return args


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

    This function prompts the user to describe an artifact, choose an ideation
    technique, specify the number of ideas to generate, select an output type,
    and choose an AI model. It ensures user inputs are validated where necessary.

    Returns:
        tuple: A tuple containing:
            - str: The artifact description provided by the user.
            - str: The selected ideation technique.
            - int: The number of ideas to generate (default is 1 if input is invalid).
            - str: The chosen output type ("Text" or "Image").
            - str: The selected AI model from predefined options.
    """
    # Prompt user to describe the artifact they want to modify
    artifact = questionary.text("Describe the artifact you want to modify:").ask()

    # Allow user to select an ideation technique from predefined choices
    technique = questionary.select(
        "Choose an ideation technique:",
        choices=[
            "Brainstorming",
            "Mind Maps",
            "Round Robin",
            "Opposite Thinking",
            "Cut-Up",
            "Mash-Up",
            "Crazy Eights",
            "SCAMPER",
        ],
    ).ask()

    # Prompt user to enter the number of ideas to generate, defaulting to 1 if invalid
    count = questionary.text("How many ideas should be generated? (Default: 1)").ask()
    count = (
        int(count) if count.isdigit() else 1
    )  # Ensure count is an integer, fallback to 1

    # Allow user to choose an AI model from predefined options
    model = questionary.select("Select an AI model:", choices=MODEL_CHOICES).ask()

    return artifact, technique, count, model


def save_args_to_json(data, dir_path):
    """Save arguments to a timestamped JSON file, ensuring the directory exists."""
    # Define file path
    json_file = os.path.join(dir_path, "metadata.json")

    # Save data to JSON
    with open(json_file, "w", encoding="utf-8") as file_obj:
        dump(data, file_obj, indent=4)

    print(f"Saved run output to {json_file}")
