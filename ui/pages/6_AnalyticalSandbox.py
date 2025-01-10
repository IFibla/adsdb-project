import streamlit as st
import pandas as pd

st.title("Analytical Sandbox")

st.markdown(
    "This code defines an AnalyticalSandbox class that acts as a foundation for moving and transforming data "
    "within an analytical system. The AnalyticalSandbox class helps create a separate space where you can "
    "prepare data specifically for analysis. This isolation from the main operational database offers "
    "several advantages:\n"
    "1. **Data Isolation**: Protects your operational data by performing transformations and analysis in a separate "
    "environment.\n"
    "2. **Performance Optimization**: Allows for data restructuring and aggregation tailored to analytical queries, "
    "improving query speed and efficiency.\n"
    "3. **Data Exploration and Experimentation**: Provides a safe space to test different data models, transformations, "
    "and analyses without impacting live systems."
)

st.write("## Safety Rating by Brand")

st.markdown(
    "It applies a filter to the extracted data, keeping only the columns that are relevant for brand "
    "analysis (_vehicle_make_, _vehicle_year_, and _overall_rating_). This focuses the data in the "
    "sandbox on specific attributes for analysis."
)


st.write("## Safety Rating by Accidents")

st.markdown(
    "For the analytical sandbox of the accident rating model, no additional modifications are required. "
    "Therefore, data will be directly copied from the exploitation zone to the analytical sandbox database "
    "without further processing."
)
