import streamlit as st

# counter = 0

# if st.button("Increment"):
#    counter += 1

# st.write(f"Counter: {counter}")


if "counter" not in st.session_state:
    st.session_state["counter"] = 0  # Initialize counter in session state

if st.button("Increment"):
    st.session_state["counter"] += 1  # Increment counter in session state

st.write(f'Counter: {st.session_state["counter"]}')
