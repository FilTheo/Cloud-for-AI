import requests
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "add_your_token"}


# Function to query Hugging Face API for text summarization
def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# Streamlit App Layout
st.title("Text Summarization using Hugging Face")

# Input text box for user to enter text
user_input = st.text_area("Enter text to summarize", "")

# Button to trigger summarization
if st.button("Summarize"):
    if user_input:
        # Call Hugging Face API
        payload = {"inputs": user_input}
        output = query(payload)

        # Check for errors in API response
        if "error" in output:
            st.error(f"An error occurred: {output['error']}")
        else:
            # Display summarized text
            st.subheader("Summarized Text")
            st.write(output[0]["summary_text"])
    else:
        st.warning("Please enter text to summarize.")
