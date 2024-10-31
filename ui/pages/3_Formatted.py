import streamlit as st
import pandas as pd
import sys
import os

st.title("Formatted")
st.write("## New York City Open Data")

with st.expander("Motor Vehicle Collisions Crash"):
    df = pd.read_csv(
        "./sample_tables/motorvehiclecollisions_crashes_2012.csv", index_col=23
    )
    st.dataframe(df)
    p = open("./profilings/crashes.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


with st.expander("Motor Vehicle Collisions Person"):
    st.dataframe(
        pd.read_csv(
            "./sample_tables/motorvehiclecollisions_person_2012.csv", index_col=1
        )
    )
    p = open("./profilings/persons.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


with st.expander("Motor Vehicle Collisions Vehicles"):
    st.dataframe(
        pd.read_csv(
            "./sample_tables/motorvehiclecollisions_vehicles_2012.csv", index_col=1
        )
    )
    p = open("./profilings/vehicles.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


st.write("## National Highway Traffic Safety Administration")
with st.expander("Vehicle Safety Rating"):
    st.dataframe(
        pd.read_csv("./sample_tables/nhtsa_safety_rating_20241027.csv", index_col=30)
    )
    p = open("./profilings/nhtsa.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)
