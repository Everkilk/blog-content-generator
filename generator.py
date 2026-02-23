import api
from google import genai
from google.genai import types


def generate_content(prompt: str) -> str:
    """Generate a blog post using Gemini with Google Search grounding."""
    client = genai.Client(api_key=api.google_api_key)
    model  = "gemini-3-flash-preview"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]
    tools  = [types.Tool(googleSearch=types.GoogleSearch())]
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
        tools=tools,
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model, contents=contents, config=config
    ):
        response_text += chunk.text
    return response_text


def generate_thumbnail(prompt_thumbnail: str) -> bytes | None:
    """Generate a 16:9 thumbnail image. Returns raw JPEG bytes or None."""
    client = genai.Client(api_key=api.google_api_key)

    result = client.models.generate_images(
        model="models/imagen-4.0-fast-generate-001",
        prompt=prompt_thumbnail,
        config=dict(
            number_of_images=1,
            output_mime_type="image/jpeg",
            person_generation="ALLOW_ADULT",
            aspect_ratio="16:9",
        ),
    )

    if not result.generated_images:
        return None
    return result.generated_images[0].image.image_bytes


def build_content_prompt(blog_title: str, keywords: str, num_words: int) -> str:
    return (
        f'Generate a comprehensive, engaging blog post relevant to the given title '
        f'"{blog_title}" and keywords "{keywords}". Make sure to incorporate these '
        f'keywords in the blog post. The blog should be approximately {num_words} words '
        f'in length, suitable for an online audience. Ensure the content is original, '
        f'informative and maintains a consistent tone throughout.'
    )


def build_thumbnail_prompt(blog_title: str) -> str:
    return (
        f'Generate a thumbnail image for a blog post titled "{blog_title}". '
        f'The image should be visually appealing and relevant to the blog topic, '
        f'incorporating elements that reflect the essence of the content. '
        f'Ensure the design is eye-catching and suitable for online platforms, '
        f'while maintaining a professional and polished look.'
    )
