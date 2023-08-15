
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Streamlit app title
st.title("Churn Analysis Dashboard")

# Sidebar for inputting dynamic costs
st.sidebar.header("Set Prices for Profit Calculation")
yes_yes_cost = st.sidebar.number_input("Yes/Yes Cost (€)", value=150000, step=1000)
yes_no_cost = st.sidebar.number_input("Yes/No Cost (€)", value=-80000, step=1000)
no_yes_cost = st.sidebar.number_input("No/Yes Cost (€)", value=-20000, step=1000)
no_no_cost = st.sidebar.number_input("No/No Cost (€)", value=3000000, step=1000)

costs = {
    'Yes/Yes': yes_yes_cost,
    'Yes/No': yes_no_cost,
    'No/Yes': no_yes_cost,
    'No/No': no_no_cost
}

# Data loading and preprocessing (based on the original code provided)
# ... (The original code you provided would be integrated here)

# Section 1: Data Exploration
st.header("Data Exploration")

# Distribution plots for Tenure and MonthlyCharges
# ... (Visualization code for distribution plots)

# Bar plots for gender and InternetService distribution
# ... (Visualization code for bar plots)

# Correlation heatmap
# ... (Visualization code for the heatmap)

# Section 2: Predictions & Model Evaluation
st.header("Predictions & Model Evaluation")

# ROC Curve and AUC Score
# ... (Visualization code for ROC curve)

# Confusion Matrix
# ... (Visualization code for confusion matrix)

# Section 3: Business Evaluation
st.header("Business Evaluation")

# Profit vs Threshold plot based on dynamic costs
# ... (Visualization code for the profit vs threshold plot)

# Customer segmentation visualizations
# ... (Visualization code for customer segmentation)

# Run the app with 'streamlit run <filename>.py'
