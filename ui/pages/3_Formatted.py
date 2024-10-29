import streamlit as st
import sys
import os

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
sys.path.insert(0, project_root)
from src.helpers.db_connector import DBConnector

formatted_db_connector = DBConnector("../data/db_formatted.duckdb")

st.title("Formatted")


st.write("## New York City Open Data")

with st.expander("Motor Vehicle Collisions Crash"):
    st.dataframe(
        formatted_db_connector.get_table_as_dataframe(
            "motorvehiclecollisions_crashes_2012", limit=10
        )
    )
    p = open("./profilings/crashes.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


with st.expander("Motor Vehicle Collisions Person"):
    st.dataframe(
        formatted_db_connector.get_table_as_dataframe(
            "motorvehiclecollisions_person_2012", limit=10
        )
    )
    p = open("./profilings/persons.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


with st.expander("Motor Vehicle Collisions Vehicles"):
    st.dataframe(
        formatted_db_connector.get_table_as_dataframe(
            "motorvehiclecollisions_vehicles_2012", limit=10
        )
    )
    p = open("./profilings/vehicles.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)


st.write("## National Highway Traffic Safety Administration")
with st.expander("Vehicle Safety Rating"):
    st.dataframe(
        formatted_db_connector.get_table_as_dataframe(
            "nhtsa_safety_rating_20241026", limit=10
        )
    )
    p = open("./profilings/nhtsa.html")
    st.components.v1.html(p.read(), scrolling=True, height=500)
