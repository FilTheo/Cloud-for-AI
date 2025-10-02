"""
Minimal OCR -> diffusion pipeline using the Hugging Face Inference API.

Before running:
1. Create a free Hugging Face account.
2. Generate a Personal Access Token with the 'Inference API' scope (Profile > Settings > Access Tokens).
3. Export it as the environment variable HF_API_TOKEN or pass it directly to the helper functions.
"""

import io
import os
from typing import Optional, Tuple

import requests
from PIL import Image

OCR_MODEL_ID = "microsoft/trocr-base-printed"
IMAGE_MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"

OCR_API_URL = f"https://api-inference.huggingface.co/models/{OCR_MODEL_ID}"
IMAGE_GEN_API_URL = f"https://api-inference.huggingface.co/models/{IMAGE_MODEL_ID}"


def require_token(token: Optional[str] = None) -> str:
    """Return a Hugging Face token or raise if it is missing."""
    candidate = (token or os.getenv("HF_API_TOKEN", "")).strip()
    if not candidate or candidate == "YOUR_HF_API_TOKEN_HERE":
        raise ValueError(
            "Please create a Hugging Face access token with the 'Inference' scope "
            "and set it via the HF_API_TOKEN environment variable or pass it directly."
        )
    return candidate


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def extract_text_from_menu(image_bytes: bytes, token: Optional[str] = None) -> str:
    """Send a menu photo to the OCR model and return the extracted text."""
    token_value = require_token(token)
    response = requests.post(
        OCR_API_URL,
        headers=_headers(token_value),
        data=image_bytes,
        timeout=60,
    )
    if response.status_code != 200:
        raise ValueError(
            f"OCR request failed with status code {response.status_code}: {response.text}"
        )

    result = response.json()
    if not isinstance(result, list) or not result:
        raise ValueError(f"OCR model returned an unexpected payload: {result}")

    generated_text = result[0].get("generated_text", "").strip()
    if not generated_text:
        raise ValueError("OCR model did not return any text. Try a clearer menu image.")
    return generated_text


def build_prompt(dish_name: str) -> str:
    """Construct a simple prompt for the diffusion model from the dish name."""
    clean_name = dish_name.strip() or "a restaurant meal"
    return (
        f"A professional, high-resolution photograph of {clean_name}, "
        "beautifully plated in a modern restaurant with natural lighting."
    )


def generate_image_from_prompt(prompt: str, token: Optional[str] = None) -> Image.Image:
    """Send a text prompt to the diffusion model and return the generated image."""
    token_value = require_token(token)
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}
    response = requests.post(
        IMAGE_GEN_API_URL,
        headers=_headers(token_value),
        json=payload,
        timeout=120,
    )
    if response.status_code != 200:
        raise ValueError(
            f"Image generation failed with status code {response.status_code}: {response.text}"
        )

    content_type = response.headers.get("Content-Type", "")
    if "image" not in content_type:
        raise ValueError(
            f"Image generation returned an unexpected payload: {response.text}"
        )

    image = Image.open(io.BytesIO(response.content))
    image.load()
    return image


def menu_to_meal(
    image_bytes: bytes, token: Optional[str] = None
) -> Tuple[str, str, str, Image.Image]:
    """
    Run the full pipeline: OCR the menu image, pick a dish, build a prompt,
    and generate an image of the meal.
    """
    extracted_text = extract_text_from_menu(image_bytes, token)
    dish = next(
        (line.strip() for line in extracted_text.splitlines() if line.strip()), ""
    )
    if not dish:
        raise ValueError("Could not identify a dish from the extracted menu text.")

    prompt = build_prompt(dish)
    generated_image = generate_image_from_prompt(prompt, token)
    return extracted_text, dish, prompt, generated_image


def main() -> None:
    try:
        token = require_token()
    except ValueError as exc:
        print(f"Token error: {exc}")
        return

    menu_image_path = (
        "path/to/your/menu.jpg"  # Update with an actual path before running.
    )
    if not os.path.exists(menu_image_path):
        print("Please update menu_image_path with a valid image file.")
        return

    with open(menu_image_path, "rb") as image_file:
        image_bytes = image_file.read()

    try:
        extracted_text, dish, prompt, generated_image = menu_to_meal(image_bytes, token)
    except (requests.exceptions.RequestException, ValueError) as exc:
        print(f"Pipeline error: {exc}")
        return

    print("Extracted text:")
    print(extracted_text)
    print(f"Dish to generate: {dish}")
    print(f"Prompt sent to the image model: {prompt}")

    output_path = "generated_meal_api.png"
    generated_image.save(output_path)
    print(f"Generated image saved as '{output_path}'")


if __name__ == "__main__":
    main()
