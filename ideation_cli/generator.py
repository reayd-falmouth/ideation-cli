import os
import json
import requests
from openai import OpenAI
from ideation_cli.prompts import get_prompt
from ideation_cli.utils import validate_model

OPENAI_CLIENT = OpenAI()
DIRNAME = os.path.dirname(__file__)

# Module-level constants for system prompts
GAME_NAME_PROMPT = (
    "You are a helpful assistant that generates concise, standalone names for video games. "
    "Your answers have no preamble or summary. Provide a title without special characters."
)

GAME_METADATA_PROMPT = (
    "You are a helpful assistant that generates metadata about video games. Your answers have no "
    "preamble or summary. Provide a short description, detailed description, and an appropriate set of tags "
    "as valid JSON: {'short_description': 'string', 'detailed_description': string, 'tags': list}"
)


def _call_openai_chat(
    model: str, messages: list, temperature: float = 1.0, top_p: float = 1.0
) -> str:
    """Helper function to call OpenAI chat completions and clean the response."""
    response = OPENAI_CLIENT.chat.completions.create(
        model=model, temperature=temperature, top_p=top_p, messages=messages
    )
    content = response.choices[0].message.content
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]
    return content.strip("```json").strip("```")


def generate_ideas(artifact: str, technique: str, model: str) -> str:
    """Generates game ideas using a given ideation technique."""
    prompt = get_prompt(artifact, technique)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that generates concise, standalone ideas. "
                "Provide your answer in plain text without markdown."
            ),
        },
        {"role": "user", "content": prompt},
    ]
    return _call_openai_chat(model, messages)


def generate_name(
    prompt: str, model: str, temperature: float = 1.0, top_p: float = 1.0
) -> str:
    """Generates a game name based on a prompt."""
    model = validate_model(model)
    messages = [
        {"role": "system", "content": GAME_NAME_PROMPT},
        {"role": "user", "content": prompt},
    ]
    return _call_openai_chat(model, messages, temperature, top_p)


def generate_metadata(
    prompt_task: str,
    prompt_name: str,
    model: str,
    temperature: float = 1.0,
    top_p: float = 1.0,
) -> dict:
    """Generates game metadata (short and detailed descriptions with tags) as a JSON object."""
    model = validate_model(model)
    messages = [
        {"role": "system", "content": GAME_METADATA_PROMPT},
        {
            "role": "user",
            "content": f"The game concept is {prompt_task}, and the name of the game is {prompt_name}. Provide the details.",
        },
    ]
    response = _call_openai_chat(model, messages, temperature, top_p)
    return json.loads(response)


def generate_image_prompt(
    prompt_task: str, prompt_name: str, model: str = "gpt-4", temperature: float = 0.7
) -> str:
    """Generates a detailed image prompt for cover art by calling the OpenAI chat API."""
    system_message = "You are a creative assistant that generates detailed image prompts for pixel art game covers."
    user_message = (
        f"Generate a detailed image prompt for a pixel art cover image for the game '{prompt_name}' with the theme '{prompt_task}'. "
        "Include style suggestions, specify that the image should be 1024x1024, and mention the essential cover requirements for itch.io (minimum 315x250, recommended 630x500)."
    )
    response = OPENAI_CLIENT.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )
    content = response.choices[0].message.content
    # Remove unintended leading/trailing quotes, if any.
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]
    return content.strip()


def generate_cover(
    prompt_task: str,
    prompt_name: str,
    dir_path: str,
    prompt_model: str = "gpt-4",
    temperature: float = 0.7,
) -> str:
    """Generates and saves a pixel art cover image for a game, returning the image path.

    It first generates a detailed image prompt using the OpenAI chat API, then uses that prompt to generate the image.
    """
    try:
        # Generate the image prompt via OpenAI Chat API.
        image_prompt = generate_image_prompt(
            prompt_task, prompt_name, model=prompt_model, temperature=temperature
        )

        # Use the generated prompt to create the image.
        response = OPENAI_CLIENT.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        image_path = os.path.join(dir_path, "cover.png")
        image_data = requests.get(image_url).content
        with open(image_path, "wb") as file:
            file.write(image_data)
        return image_path
    except Exception as err:
        raise RuntimeError("Failed to generate cover image") from err
