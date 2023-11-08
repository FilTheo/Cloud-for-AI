import streamlit as st

# import pandas as pd


###############################
# App initializations

configurations = {}
configurations["whatever"] = None

###############################
# Streamlit initializations
# Session states
if "df" not in st.session_state:
    st.session_state.df = None
if "original_df" not in st.session_state:
    st.session_state.original_df = None
if "features" not in st.session_state:
    st.session_state.features = None
if "configurations" not in st.session_state:
    st.session_state.configurations = configurations

##################################
# Sidebar

# Add an expander to load data
st.sidebar.title("1. Data Selection")
with st.sidebar.expander("Dataset", expanded=True):
    ...


# Pick the temporal level
st.sidebar.title("2. Temporal Level Selection")
with st.sidebar.expander("Temporal level", expanded=True):
    ...

# Filter the time series
st.sidebar.title("3. Time Series Filtering")
with st.sidebar.expander("Filter time series", expanded=True):
    ...

####################################
# Main

st.header("Time Series Dashboard")
st.write("Here you will add your fancy marketing text")
