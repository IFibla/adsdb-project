from sklearn.experimental import enable_iterative_imputer
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
    st.session_state["sandbox"] = True
    st.session_state["feature"] = True
    st.session_state["train"] = True
    st.session_state["validate"] = True
    st.session_state["validation_result"] = None

dataops = DataOps(
    temporal_folder="ui/simulation/landing/temporal/",
    persistent_folder="ui/simulation/landing/persistent/",
    connector_folder="ui/simulation/",
)

st.title("Simulation")

st.warning(
    "As we are working with sample dataset is is normal to find null values in layers like Trusted or Exploitation."
)

st.markdown(
    """
This page enables the execution of the entire data backbone pipeline, with four dedicated buttons—Landing, Formatted, 
Trusted, and Exploitation—each responsible for processing a specific layer. Clicking on **Landing** organizes and moves 
datasets from a temporary area to a persistent landing, where results can be viewed in specific folders. Since files 
are removed from the temporary landing, it’s recommended to copy them to another location for experiment reproduction. 
The **Formatted** button prepares and standardizes data, **Trusted** applies quality checks for reliability, and 
**Exploitation** finalizes the data for end use. Additionally, a database selector allows users to navigate different 
databases, viewing tables and data across each layer of the pipeline, offering a streamlined, step-by-step approach to 
data management."""
)

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
        st.session_state["sandbox"] = False

col11, col12, col13, col14 = st.columns(4)

with col11:
    if st.button(
        "Execute Analytical Sandbox",
        use_container_width=True,
        disabled=st.session_state["sandbox"],
    ):
        with st.spinner("Computing Analytical Sandbox..."):
            dataops.execute_stage("analytical_sandbox")
        st.session_state["sandbox"] = True
        st.session_state["feature"] = False


with col12:
    if st.button(
        "Execute Feature Engineering",
        use_container_width=True,
        disabled=st.session_state["feature"],
    ):
        with st.spinner("Computing Feature Engineering..."):
            dataops.execute_stage("feature_engineering")
        st.session_state["feature"] = True
        st.session_state["train"] = False

with col13:
    if st.button(
        "Execute Model Training",
        use_container_width=True,
        disabled=st.session_state["train"],
    ):
        with st.spinner("Computing model training..."):
            dataops.execute_stage("training")
        st.session_state["train"] = True
        st.session_state["validate"] = False

with col14:
    if st.button(
        "Execute Model Validation",
        use_container_width=True,
        disabled=st.session_state["validate"],
    ):
        with st.spinner("Computing model validation..."):
            st.session_state["validation_result"] = dataops.execute_stage("validation")
            print(st.session_state["validation_result"])
        st.session_state["validate"] = True

layer = st.radio(
    "Layer Database chooser.",
    [
        "Formatted",
        "Trusted",
        "Exploitation",
        "Analytical Sandbox",
        "Feature Engineering",
    ],
    horizontal=True,
)
table = st.radio(
    "Tables.",
    dataops.pipeline.connectors[
        f"{layer.lower().replace(' ', '_')}_connector"
    ].get_tables(),
    horizontal=True,
)

if table is not None:
    st.dataframe(
        dataops.pipeline.connectors[
            f"{layer.lower().replace(' ', '_')}_connector"
        ].get_table_as_dataframe(table, limit=20)
    )

if st.session_state["validation_result"] is not None:
    st.json(st.session_state["validation_result"])
