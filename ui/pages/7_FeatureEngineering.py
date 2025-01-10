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

st.markdown(
    "The Accident Feature Engineering layer modifies the data to prepare it for machine learning. Vehicle age "
    "is calculated from the manufacturing year, and the original year column is removed to simplify the dataset. "
    "Vehicle make is transformed into numerical embeddings, which better represent categorical information for "
    "the model, and the original make column is dropped. Overall ratings are standardized by limiting their range "
    "to 0-5 and rounding them to the nearest 0.5 for consistency.\n\nTo address missing data, iterative imputation "
    "is applied to fill gaps in age, gender, and ratings, ensuring the dataset is complete. Gender is first encoded "
    "as numeric values and then converted into one-hot encoding to enhance its usability for machine learning "
    "algorithms. Irrelevant columns, such as IDs, are removed to avoid unnecessary noise. Data types, like age, are "
    "adjusted to ensure consistency and compatibility with the modeling process. These transformations result in a "
    "clean, structured dataset ready for analysis."
    ""
)
