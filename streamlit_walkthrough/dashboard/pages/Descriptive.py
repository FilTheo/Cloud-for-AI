import streamlit as st


###########################################
# Page specific Initializations
if "sample_to_plot" not in st.session_state:
    st.session_state.sample_to_plot = None

# Initialize seasonality on st.session_confugurations
if "seasonality" not in st.session_state.configurations:
    st.session_state.configurations["seasonality"] = 12


###########################################
# Prepare the sidebar
st.sidebar.title("Reset Filters")
with st.sidebar.expander("Reset Filters", expanded=True):
    # Write some text: if you clikc the button blah blah you reset
    st.write("Push the button to reset filters of the loaded dataset")

    # Add a button to reset filters. If the user clicks it I reload the original_df
    if st.button("Reset filters"):
        st.session_state.df = st.session_state.original_df
        # In the configurations too
        st.session_state.configurations["df"] = st.session_state.original_df

# Pick the temporal level
st.sidebar.title("2. Temporal Level Selection")
with st.sidebar.expander("Temporal level", expanded=True):
    ...

# Filter the time series
st.sidebar.title("3. Time Series Filtering")
with st.sidebar.expander("Filter time series", expanded=True):
    ...


###########################################
# Prepar the main


# Define the tabs
tab1, tab2 = st.tabs(["CEO", "DEMAND PLANNER"])
# CEO tab
with tab1:
    # First line with plots
    st.subheader("First line of plots")
    st.write("show some plot")

    st.divider()

    # Second line here
    st.subheader("Second line of plots")

    # Two columns
    col1, col2 = st.columns(2)

    # First column
    with col1:
        st.write("First column")
        st.write("show some plot")

    # Second column
    with col2:
        st.write("Second column")
        st.write("show some plot")

    st.divider()

    # Third line here
    st.subheader("Third line of plots")
    st.write("show some plot")

with tab2:
    st.header("Maybe some extra plots here")
