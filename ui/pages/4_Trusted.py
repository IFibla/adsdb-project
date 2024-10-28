import streamlit as st
import sys
import os

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
sys.path.insert(0, project_root)
from src.helpers.db_connector import DBConnector

trusted_db_connector = DBConnector("../data/db_trusted.duckdb")

st.write("# Motor Vehicle Collisions")

st.dataframe(trusted_db_connector.get_table_as_dataframe("mvc_crash", limit=10))

st.dataframe(trusted_db_connector.get_table_as_dataframe("mvc_person", limit=10))

st.dataframe(trusted_db_connector.get_table_as_dataframe("mvc_vehicles", limit=10))
st.write("# Vehicle Safety Rating")

st.dataframe(
    trusted_db_connector.get_table_as_dataframe("nhtsa_safety_rating", limit=10)
)
