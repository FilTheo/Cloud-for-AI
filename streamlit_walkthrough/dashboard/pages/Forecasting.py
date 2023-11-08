import streamlit as st
import time

#################################
# Initializations

if "fc_models" not in st.session_state:
    st.session_state.fc_models = None
if "fc_horizon" not in st.session_state:
    st.session_state.fc_horizon = None
if "dummy_not_cv" not in st.session_state:
    st.session_state.dummy_not_cv = None
if "fc_cv" not in st.session_state:
    st.session_state.fc_cv = 1
if "fc_launch" not in st.session_state:
    st.session_state.fc_launch = None
if "fc_finished" not in st.session_state:
    st.session_state.fc_finished = None
if "fc_holdout" not in st.session_state:
    st.session_state.fc_holdout = None
if "fc_results" not in st.session_state:
    st.session_state.fc_results = None
if "fc_evaluations" not in st.session_state:
    st.session_state.fc_evaluations = None

#################################
# Sidebar

# General title
st.sidebar.title("Pick your preferences")

# Tickbox to evalaute
st.session_state.fc_holdout = st.sidebar.checkbox("Evaluate Forecasting", value=True)
st.session_state.configurations["fc_holdout"] = st.session_state.fc_holdout

# First section
st.sidebar.title("Set Up Forecasting")

# Model selection
with st.sidebar.expander("Model Selection", expanded=True):
    # Widget for multiselect
    st.session_state.fc_models = st.multiselect(
        "Select the models to use", ["ETS", "ARIMA", "Naive", "SNaive", "CrostonOptimized"], default=["ETS"]
    )

    # Add to the dictionary
    st.session_state.configurations["fc_models"] = st.session_state.fc_models


with st.sidebar.expander("Forecast Horizon", expanded=True):
    # Widget for multiselect
    st.session_state.fc_horizon = st.slider("Set the forecast horizon", min_value=1, max_value=24, value=12)

    # Add to the dictionary
    st.session_state.configurations["fc_horizon"] = st.session_state.fc_horizon


with st.sidebar.expander("Cross Validation"):
    # checkbox if we do cross validation
    st.session_state.dummy_not_cv = st.checkbox("Cross Validation", value=False)
    if st.session_state.dummy_not_cv:
        # Add to the dictionary
        st.session_state.configurations["fc_dummy_cv"] = st.session_state.dummy_not_cv

        # Add a slider for the number of folds
        st.session_state.fc_cv = st.slider("Set the number of folds", min_value=1, max_value=5, value=1)

        # Add to the dictionary
        st.session_state.configurations["fc_cv"] = st.session_state.fc_cv

    else:
        st.session_state.configurations["fc_cv"] = None

# Metrics
with st.sidebar.expander("Metrics"):
    # Checkbox for metrics
    st.session_state.configurations["fc_metrics"] = st.multiselect(
        "Pick the Evaluation Metrics",
        ["MAE", "MSE", "RMSE", "SMAPE", "MASE", "RMSSE"],
        default=["MAE", "MSE", "RMSSE"],
    )


###################################
# Main page

# Add an expander with a message for forecasrting
with st.expander("Build a Forecasting Model"):
    st.write("Here some description on how to do forecasting")

# A checkbox to launch forecasting
st.session_state.fc_launch = st.checkbox("Launch Forecasting", value=False)

if st.session_state.fc_launch:
    # Add a timer for the forecasting
    with st.spinner("Forecasting in progress..."):
        # Add a timer
        time.sleep(10)
        # Say that forecasts are completed
        st.session_state.fc_finished = True


# IF the forecasts are completed
if st.session_state.fc_finished:
    # Split on two tabs
    tab1, tab2 = st.tabs(["Forecasting", "Evaluation"])

    with tab1:
        st.subheader("Pick your plotting preference")
        # Split the widgets into two columns
        col1, col2 = st.columns(2)
        with col1:
            selected_for_vis = st.selectbox(
                "Select the part of the time serise to plot", ["Full", "In-Sample", "Out-of-Sample"]
            )
        with col2:
            total_ts = 30
            max_factor = max([i for i in range(1, total_ts + 1) if total_ts % i == 0])

        st.divider()

        st.write("Here you will plot something")

    with tab2:
        # First line the overview
        st.subheader("Overall model performance")

        st.write("Here just show some plots to evaluate")
