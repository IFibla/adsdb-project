import streamlit as st
import pandas as pd

st.title("Feature Engineering")

st.markdown(
    "Feature engineering is a critical step in preparing data for machine learning. It involves transforming raw "
    "data into meaningful features that machine learning algorithms can understand and utilize.\n"
    "1. **Data Understanding**. This includes analyzing its structure, identifying variables and their relationships, "
    "and clearly defining the prediction target to guide feature engineering efforts.\n"
    "2. **Feature Creation**. This involves brainstorming potential features based on data understanding and the "
    "prediction target, then extracting them from the raw data by combining, decomposing, or aggregating existing "
    "features.\n"
    "3. **Feature Transformation**. This includes scaling numerical features, encoding categorical features, and "
    "handling missing values."
)

st.write("## Safety Rating by Brand")

st.markdown(
    "This code performs feature engineering on a DataFrame containing vehicle data. It starts by calculating the "
    "age of the vehicle and normalizing its overall rating. Then, it generates numerical representations "
    "(embeddings) for the vehicle make and adds them as new features. Any rows with missing data are removed. "
    "Finally, the code selects a subset of the engineered features, including the embeddings, vehicle age, and "
    "normalized rating, likely for use in a machine learning model."
)

st.write("## Safety Rating by Accidents")
