"""
generator.py - AI-Powered Content Generation for Ideation CLI.

This module provides functions to generate game ideas, branding, and cover images
using OpenAI's API. It supports multiple ideation techniques and metadata generation
for game development projects.

Functions:
    - generate_ideas(artifact, technique, count, output, model):
      Creates game-related ideas based on user-defined ideation techniques.
    - generate_name(prompt, model):
      Generates a game name based on a given prompt.
    - generate_branding(prompt_task, prompt_name, model):
      Produces game branding metadata, including descriptions and tags.
    - generate_cover(prompt_task, prompt_name, dir_path):
      Generates and saves a pixel art cover image using DALL·E.

Constants:
    - OPENAI_CLIENT: OpenAI API client instance.
    - DIRNAME: Path to the current module's directory.

Dependencies:
    - os
    - json
    - requests
    - openai
    - ideation_cli.prompts (for structured idea prompts)
    - ideation_cli.utils (for input validation)

Usage:
    ```python
    from generator import generate_name

    name = generate_name("A strategy game about space exploration")
    print(name)
    ```
"""

import os

import openai
import requests
from openai import OpenAI

from ideation_cli.prompts import get_prompt
from ideation_cli.utils import validate_model

OPENAI_CLIENT = OpenAI()
DIRNAME = os.path.dirname(__file__)


def generate_ideas(artifact, technique, count, model):
    """Generates remediation's using OpenAI API and Autogen."""

    prompt = get_prompt(artifact, technique)
    responses = []

    for _ in range(count):
        completion = OPENAI_CLIENT.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates concise, standalone "
                    "ideas. Your answers have no preamble or summary. You provide them in "
                    "text only without markdown.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        responses.append(completion.choices[0].message.content)

    print("\nGenerated Ideas:\n" + "\n".join(responses))


def generate_name(prompt, model):
    """Generates remediation's using OpenAI API and Autogen."""
    model = validate_model(model)

    try:
        completion = OPENAI_CLIENT.chat.completions.create(
            model=model,
            temperature=0.7,
            top_p=0.8,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates concise, standalone "
                    "names for video games. Your answers have no preamble or summary. "
                    "You provide them in text only without markdown.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        response = completion.choices[0].message.content

        # Remove any unintended leading/trailing quotes
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]

        return response
    except Exception as err:
        print(err)


def generate_metadata(prompt_task, prompt_name, model):
    """Generates remediation's using OpenAI API and Autogen."""
    model = validate_model(model)

    try:
        completion = OPENAI_CLIENT.chat.completions.create(
            model=model,
            temperature=0.7,
            top_p=0.8,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates metadata about video games."
                    "Your answers have no preamble or summary. "
                    "You provide a short description, detailed description, and appropriate set of tags."
                    "The response should be valid json of the form "
                    "{'short_description': 'string', 'detailed_description': string, 'tags': list}",
                },
                {
                    "role": "user",
                    "content": f"The game concept is {prompt_task}, and the name of the game is {prompt_name}, "
                    f"Provide the details for this game.",
                },
            ],
        )

        response = completion.choices[0].message.content

        # Remove any unintended leading/trailing quotes
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]

        response = response.strip("```json").strip("```")

        return response
    except Exception as err:
        print(err)


def generate_cover(prompt_task, prompt_name, dir_path):
    """Generate and save a pixel art cover image for a game, ensuring the directory exists."""

    # Generate the image prompt
    prompt = (
        f"Generate a pixel art cover image for the game {prompt_name} {prompt_task} "
        f"a project for itch.io. The specifications are as follows: "
        f"The cover image is used whenever itch.io wants to link to your project "
        f"from another part of the site. Required (Minimum: 315x250, Recommended: 630x500)."
    )

    try:
        # Request image generation from OpenAI
        response = OPENAI_CLIENT.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Retrieve image URL
        image_url = response.data[0].url

        # Define image file path
        image_path = os.path.join(dir_path, "cover.png")

        # Download and save the image
        image_data = requests.get(image_url).content
        with open(image_path, "wb") as file:
            file.write(image_data)

        print(f"Image saved as {image_path}")

    except Exception as err:
        print(err)
