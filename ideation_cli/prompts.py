"""
prompt_generator.py - Generates prompts for ideation techniques.

This module provides functions to generate structured prompts based on
different creative ideation methods.

Functions:
    - get_prompt(artifact, technique): Returns a formatted prompt based
      on the selected ideation technique.

Usage:
    ```python
    from prompt_generator import get_prompt

    prompt = get_prompt("a new board game", "mash_up")
    print(prompt)  # Output: Combine a new board game with another
                   # unrelated concept to create an innovative outcome.
    ```
"""

GAME_NAME_PROMPT = (
    "You are a creative naming assistant. Generate concise, standalone names for video game jams. "
    "Avoid clichés and over-used words—vary your vocabulary and explore unexpected combinations. "
    "Think outside the box: use vivid imagery, playful wordplay or surprising contrasts. "
    "Answer with only the name, no preamble or summary."
)

GAME_METADATA_PROMPT = (
    "You are a helpful assistant that generates metadata about video games. Your answers have no "
    "preamble or summary. Provide a short description, detailed description, and an appropriate set of tags "
    'as valid JSON: {"short_description": str, "detailed_description": str, "tags": list}'
)

def get_prompt(artifact, technique):
    """Returns a prompt template based on the selected ideation technique."""
    templates = {
        "brainstorming": f"Generate creative variations of {artifact} using brainstorming techniques.",
        "mind_maps": f"Create a structured mind map representation of {artifact} with multiple branches.",
        "round_robin": f"Iteratively refine {artifact} by applying team-based idea evolution.",
        "opposite_thinking": f"Identify core assumptions of {artifact} and invert them to generate new ideas.",
        "cut_up": f"Remix and cut up the components of {artifact} into a new creative format.",
        "mash_up": f"Combine {artifact} with another unrelated concept to create an innovative outcome.",
        "crazy_eights": f"Generate eight rapid-fire variations of {artifact} in a time-constrained way.",
        "scamper": f"Apply the SCAMPER technique (substitute, combine, adapt, modify, put to other uses, "
        f"eliminate, rearrange) to {artifact}.",
    }
    return (
        templates.get(technique, f"Generate creative ideas based on {artifact}."),
        technique,
    )
