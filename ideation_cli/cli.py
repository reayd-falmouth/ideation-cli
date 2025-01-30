import questionary
from ideation_cli.generator import generate_ideas

MODEL_CHOICES = [
    # "gpt-4o-audio-preview-2024-10-01",
    # "gpt-4o-mini-audio-preview",
    # "gpt-4o-mini-audio-preview-2024-12-17",
    # "gpt-4o-mini-realtime-preview",
    # "dall-e-2",
    # "gpt-3.5-turbo",
    # "o1-preview-2024-09-12",
    # "gpt-3.5-turbo-0125",
    # "o1-preview",
    # "gpt-3.5-turbo-instruct",
    # "babbage-002",
    # "gpt-4o-2024-11-20",
    # "o1-mini-2024-09-12",
    # "whisper-1",
    # "dall-e-3",
    # "chatgpt-4o-latest",
    # "gpt-4o-realtime-preview-2024-10-01",
    # "gpt-4-1106-preview",
    # "omni-moderation-latest",
    # "omni-moderation-2024-09-26",
    # "gpt-4o-2024-08-06",
    # "tts-1-hd-1106",
    "gpt-4o",
    "gpt-4",
    # "gpt-4-0613",
    # "tts-1-hd",
    # "gpt-4o-mini-2024-07-18",
    "gpt-4o-mini",
    # "davinci-002",
    # "gpt-4o-2024-05-13",
    # "text-embedding-ada-002",
    # "gpt-4-turbo",
    # "tts-1",
    # "tts-1-1106",
    # "gpt-3.5-turbo-instruct-0914",
    # "gpt-4-turbo-preview",
    # "gpt-4o-mini-realtime-preview-2024-12-17",
    # "gpt-4o-audio-preview",
    # "text-embedding-3-small",
    # "gpt-4-turbo-2024-04-09",
    # "gpt-3.5-turbo-1106",
    # "gpt-3.5-turbo-16k",
    # "gpt-4o-audio-preview-2024-12-17",
    # "gpt-4o-realtime-preview-2024-12-17",
    # "gpt-4o-realtime-preview",
    # "gpt-4-0125-preview",
    "o1-mini",
    # "text-embedding-3-large",
]


def cli():
    """Command-line interface for ideation techniques."""

    artifact = questionary.text("Describe the artifact you want to modify:").ask()

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

    count = questionary.text("How many ideas should be generated? (Default: 1)").ask()
    count = int(count) if count.isdigit() else 1  # Fallback to 10 if input is invalid

    output = questionary.select("Select output type:", choices=["Text", "Image"]).ask()

    model = questionary.select("Select an AI model:", choices=MODEL_CHOICES).ask()

    generate_ideas(
        artifact, technique.lower().replace(" ", "_"), count, output.lower(), model
    )


if __name__ == "__main__":
    cli()
