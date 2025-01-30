from openai import OpenAI

from ideation_cli.prompts import get_prompt

client = OpenAI()


def generate_ideas(artifact, technique, count, output, model):
    """Generates remediation's using OpenAI API and Autogen."""

    prompt = get_prompt(artifact, technique)
    responses = []

    for _ in range(count):
        completion = client.chat.completions.create(
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

    if output == "image":
        generate_images(artifact, responses)


def generate_images(artifact, descriptions):
    """Uses DALL·E to generate images based on text descriptions."""

    for desc in descriptions:
        short_prompt = desc[:1000]  # Truncate to 1000 characters
        print(
            f"Generating image with prompt: {short_prompt[:100]}..."
        )  # Show only the first 100 chars

        try:
            response = client.images.generate(
                prompt=short_prompt, n=1, size="1024x1024"
            )
            print(f"Image generated: {response['data'][0]['url']}")
        except Exception as e:
            print(f"Error generating image: {e}")
