import streamlit as st
import sys
import os
import io

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, "..", ".."))
sys.path.insert(0, project_root)
from dataops import DataOps

if "landing" not in st.session_state:
    st.session_state["landing"] = False
    st.session_state["formatted"] = True
    st.session_state["trusted"] = True
    st.session_state["exploitation"] = True

dataops = DataOps(
    temporal_folder="./simulation/landing/temporal/",
    persistent_folder="./simulation/landing/persistent/",
    connector_folder="./simulation/",
)

st.title("Simulation")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(
        "Execute Landing",
        use_container_width=True,
        disabled=st.session_state["landing"],
    ):
        with st.spinner("Computing Landing..."):
            dataops.execute_stage("landing")
        st.session_state["landing"] = True
        st.session_state["formatted"] = False


with col2:
    if st.button(
        "Execute Formatted",
        use_container_width=True,
        disabled=st.session_state["formatted"],
    ):
        with st.spinner("Computing Formatted..."):
            dataops.execute_stage("formatted")
        st.session_state["formatted"] = True
        st.session_state["trusted"] = False

with col3:
    if st.button(
        "Execute Trusted",
        use_container_width=True,
        disabled=st.session_state["trusted"],
    ):
        with st.spinner("Computing Trusted..."):
            dataops.execute_stage("trusted")
        st.session_state["trusted"] = True
        st.session_state["exploitation"] = False

with col4:
    if st.button(
        "Execute Exploitation",
        use_container_width=True,
        disabled=st.session_state["exploitation"],
    ):
        with st.spinner("Computing Exploitation..."):
            dataops.execute_stage("exploitation")
        st.session_state["exploitation"] = True

layer = st.radio(
    "Layer Database chooser.",
    ["Formatted", "Trusted", "Exploitation"],
    horizontal=True,
)
table = st.radio(
    "Tables.",
    dataops.pipeline.connectors[f"{layer.lower()}_connector"].get_tables(),
    horizontal=True,
)

if table is not None:
    st.dataframe(
        dataops.pipeline.connectors[
            f"{layer.lower()}_connector"
        ].get_table_as_dataframe(table, limit=20)
    )
