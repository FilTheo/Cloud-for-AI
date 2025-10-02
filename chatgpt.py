from openai import OpenAI
import streamlit as st


# Link: https://platform.openai.com/docs/quickstart?context=python

st.title("ChatGPT-like clone")

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # This is the API for using the OpenAI chat endpoint
        # More details here: https://platform.openai.com/docs/quickstart?context=python
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            # Get the response
            answer = response.choices[0].delta.content
            if answer != None:
                full_response += answer

            message_placeholder.markdown(full_response + "▌")
        # You can modify the full_response and do anything you want
        # For example I will add a " hahah" to make some fun
        full_response += " hahah"
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
