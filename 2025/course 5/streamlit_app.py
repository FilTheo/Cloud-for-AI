"""Simple Streamlit demo for the menu-to-meal pipeline."""

import io

import requests
import streamlit as st
from PIL import Image

from simple_script import menu_to_meal, require_token


st.set_page_config(page_title="Menu to Meal", page_icon="🍽️")

st.title("Menu to Meal Generator")
st.write(
    "Upload or capture a photo of a restaurant menu, we will extract a dish and "
    "generate a matching meal image using free Hugging Face models."
)

with st.expander("What you need", expanded=True):
    st.markdown(
        "- Create a free Hugging Face account.\n"
        "- Generate a Personal Access Token with the **Inference API** scope.\n"
        "- Paste the token below or set `HF_API_TOKEN` in your environment before launching the app."
    )

token_input = st.text_input(
    "Hugging Face token (leave blank to use HF_API_TOKEN env variable)",
    type="password",
)

st.write("### Step 1 · Provide a menu photo")
menu_camera = st.camera_input("Take a picture of the menu")
menu_upload = st.file_uploader("...or upload a menu image", type=["png", "jpg", "jpeg"])

menu_file = menu_camera or menu_upload

if st.button("Generate meal image"):
    if not menu_file:
        st.error("Please capture or upload a menu image first.")
        st.stop()

    image_bytes = menu_file.getvalue()

    try:
        resolved_token = require_token(token_input or None)
    except ValueError as token_error:
        st.error(str(token_error))
        st.stop()

    with st.spinner("Running OCR..."):
        try:
            extracted_text, dish, prompt, generated_image = menu_to_meal(
                image_bytes, resolved_token
            )
        except ValueError as value_error:
            st.error(str(value_error))
            st.stop()
        except requests.exceptions.RequestException as request_error:
            st.error(f"Network error: {request_error}")
            st.stop()

    st.success("Done! Here's what we found:")
    st.write("### Extracted menu text")
    st.text(extracted_text)

    st.write("### Dish used for image generation")
    st.info(dish)

    st.write("### Prompt sent to the diffusion model")
    st.code(prompt)

    st.write("### Generated meal")
    st.image(generated_image, caption="AI-generated meal")

    with st.expander("Menu image you provided"):
        st.image(Image.open(io.BytesIO(image_bytes)), caption="Original menu")
