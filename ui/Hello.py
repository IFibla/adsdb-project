import streamlit as st

st.set_page_config(
    page_title="ASDBD",
    page_icon="👋",
)

st.write("# Algorithms, Data Structures and Databases")

st.sidebar.header("Contact Information")
st.sidebar.text("Ignasi Fibla Figuerola")
st.sidebar.text("Ferran Gonzalez Garcia")

st.image("./dataBackbone.png", caption="Data Backbone")

st.markdown(
    """

"""
)

st.image("./classDiagram.png", caption="Class Diagram")

st.markdown(
    """    
In the previous diagram a structured data processing system is presented. It contains distinct layers for handling data storage, 
transformation, and exploitation. The `Layer` base class provides a generic `execute` method, while `Trusted`, 
`Formatted`, and `Exploitation` layers extend its functionality for specific tasks. The `Trusted` layer includes 
extensive data cleaning and transformation methods, the `Formatted` layer focuses on file handling, and the 
`Exploitation` layer enables data aggregation and joins for analysis. Specific data sources and formats, like CSV 
and JSON, have specialized classes under the `Formatted` layer, while `Trusted` classes manage detailed data 
operations for the different sources. 
"""
)
