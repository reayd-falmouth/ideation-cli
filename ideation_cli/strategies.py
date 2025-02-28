"""
strategies.py - Game Prompt and Oblique Strategy Utilities for the Ideation CLI.

This module provides functions to generate randomized game development prompts
and apply Brian Eno's Oblique Strategies to game design.

Functions:
    - generate_random_game_prompt(): Generate a random classic game development prompt.
    - apply_oblique_strategy(prompt): Modify a prompt by applying a random Oblique Strategy.

Constants:
    - DIRNAME: The directory path for loading configuration files.

Dependencies:
    - os
    - random
    - ideation_cli.utils.load_json

Usage:
    Import and use these functions to enhance game ideation:

    ```python
    from ideation_cli.strategies import generate_random_game_prompt, apply_oblique_strategy

    prompt, game = generate_random_game_prompt()
    modified_prompt = apply_oblique_strategy(prompt)
    ```
"""

import os
import random

from ideation_cli.utils import load_json
from ideation_cli.prompts import get_prompt

# Define the directory name for loading configuration files
DIRNAME = os.path.dirname(os.path.abspath(__file__))


def generate_random_game_prompt(game_type: str = None):
    """Generate a random game development prompt.

    This function selects a classic game from a predefined JSON file
    and constructs a prompt to develop a basic version of that game.

    Returns:
        tuple: A tuple containing:
            - str: A generated prompt string.
            - str: The name of the selected classic game.
    """
    print("Randomizing game prompt...")

    # Load the list of classic games from the JSON configuration file
    classic_games = load_json(f"{DIRNAME}/config/classic_games.json")["classic_games"]

    # Randomly select a game from the list
    if game_type is None:
        game_type = random.choice(classic_games)

    # Construct the game development prompt
    prompt = f"Develop a basic '{game_type}' game."

    return prompt, game_type


def apply_oblique_strategy(prompt):
    """
    Modifies the given prompt by applying a randomly selected oblique strategy.

    The function loads a list of oblique strategies from a JSON configuration file
    and appends a randomly chosen strategy to the input prompt.

    Args:
        prompt (str): The initial prompt that needs modification.

    Returns:
        str: The modified prompt incorporating the oblique strategy.
    """
    print("Apply oblique strategy...")

    # Load the list of oblique strategies from the JSON configuration file
    oblique_strategies = load_json(f"{DIRNAME}/config/oblique_strategies.json")[
        "oblique_strategies"
    ]

    # Select a random strategy from the list
    strategy = random.choice(oblique_strategies)

    # Append the selected strategy to the prompt
    prompt += f" Modify it by applying the oblique strategy: '{strategy}'."

    return prompt


def apply_ideation_technique(prompt, technique):
    if technique == "oblique_strategy":
        new_prompt = apply_oblique_strategy(prompt)
    else:
        new_prompt = get_prompt(prompt, technique)
    return new_prompt
