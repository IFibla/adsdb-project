import streamlit as st
import sys
import os

from mpmath import limit

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
sys.path.insert(0, project_root)
from src.helpers.db_connector import DBConnector

formatted_db_connector = DBConnector("../data/db_formatted.duckdb")

st.write("# Motor Vehicle Collisions")

st.dataframe(
    formatted_db_connector.get_table_as_dataframe(
        "motorvehiclecollisions_crashes_2012", limit=10
    )
)

st.dataframe(
    formatted_db_connector.get_table_as_dataframe(
        "motorvehiclecollisions_person_2012", limit=10
    )
)

st.dataframe(
    formatted_db_connector.get_table_as_dataframe(
        "motorvehiclecollisions_vehicles_2012", limit=10
    )
)
st.write("# Vehicle Safety Rating")

st.dataframe(
    formatted_db_connector.get_table_as_dataframe(
        "nhtsa_safety_rating_20241026", limit=10
    )
)
