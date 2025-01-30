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
        "scamper": f"Apply the SCAMPER technique (substitute, combine, adapt, modify, put to other uses, eliminate, rearrange) to {artifact}.",
    }
    return templates.get(technique, f"Generate creative ideas based on {artifact}.")
