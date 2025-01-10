import streamlit as st
import pandas as pd
import sys
import os

st.title("Trusted")

st.markdown(
    """
Any trusted layer must be initialized while adhering to the framework we have put in place. In order to allow 
for flexibility in the final implementation, we specify the connector with the formatted and trusted database. 
These connectors facilitate efficient data extraction from the formatted source and insertion into the trusted 
destination.

In this implementation, the trusted layer includes several internal methods that systematically
prepare and clean the data for analysis. It begins with the `_list_tables()` method, which retrieves all table names
from the formatted database. Next, a method standardizes the column names across all datasets by converting them
to snake_case. This standardization enhances consistency and readability, making it easier to reference columns in the
code and reducing the likelihood of errors due to inconsistent naming conventions. Next, a method consolidates multiple
tables into a single DataFrame by concatenating them. In order to avoid data duplications, all those duplicated entries
are eliminated, maintaining data integrity and preventing skewed results in analyses.

The following steps aim to identify and correct any misspelled entries within the categorical columns. This process
ensures consistency, especially when grouping or aggregating data based on categorical variables. Also, data formatting
is applied, with methods like adjusting data types, formatting dates, or transforming multiple label encodings with the same
possible values to one hot, as it would make it easy to find correlations and patterns in future analysis. Finally,
missing data and column selection processes are applied in order to delete irrelevant information.

In summary, the `Trusted` class serves as a robust and flexible layer within a data pipeline, ensuring that data is 
methodically processed, cleaned, and validated before being stored in a trusted repository. Its structured approach, 
combined with customizable methods for data cleaning and profiling, makes it an essential tool for maintaining high 
data quality standards in complex data environments.
"""
)


st.write("## Motor Vehicle Collisions")

with st.expander("Motor Vehicle Collisions Crash"):
    st.dataframe(pd.read_csv("ui/sample_tables/mvc_crash.csv", index_col=9))
    p = open("ui/profilings/mvc_crash.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


with st.expander("Motor Vehicle Collisions Person"):
    st.dataframe(pd.read_csv("ui/sample_tables/mvc_person.csv", index_col=1))
    p = open("ui/profilings/mvc_person.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


with st.expander("Motor Vehicle Collisions Vehicles"):
    st.dataframe(pd.read_csv("ui/sample_tables/mvc_vehicles.csv", index_col=1))
    p = open("ui/profilings/mvc_vehicles.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


st.write("## National Highway Traffic Safety Administration")
with st.expander("Vehicle Safety Rating"):
    st.dataframe(pd.read_csv("ui/sample_tables/nhtsa_safety_rating.csv"))
    p = open("ui/profilings/nhtsa_safety_rating.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)
