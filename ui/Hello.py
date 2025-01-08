import streamlit as st

st.set_page_config(
    page_title="ASDBD",
    page_icon="👋",
)

st.write("# Algorithms, Data Structures and Databases")

st.sidebar.header("Contact Information")
st.sidebar.text("Ignasi Fibla Figuerola")
st.sidebar.text("Ferran Gonzalez Garcia")

st.markdown(
    """
The data management backbone stands as the main module of this project. This module should manage the data process that 
goes from obtaining the raw datasets, to the exploitation zone showing crossed results between the datasets.
"""
)

st.image("./dataBackbone.png", caption="Data Backbone")

st.markdown(
    """
Previous figure shows the project's flow, where the datasources are located on the top left side of the 
diagram. It shows how information firstly arrives to the temporal landing, where it is afterwards located in the 
persistent **Landing Zone**. In second place, the different datasets go through a process where its format is 
standardized and adapted to work with pandas Dataframes and DuckDB, called the **Formatted Zone**. In the top 
right side of the diagram the next area, called the **Trusted Zone**, where data is joined through different 
versions and applied some operations to the data such as the correction of misspellings or the imputation of null 
values, if required. Finally, the **Exploitation Zone** will show tables which will help analyse and give a 
response to the questions formulated at the beginning of the project.

"""
)

st.image("./classDiagram.png", caption="Class Diagram")

st.markdown(
    """    
Finally, the upper diagram shows a structured data processing system is presented. It contains distinct storage for handling data storage, 
transformation, and exploitation. The `Layer` base class provides a generic `execute` method, while `Trusted`, 
`Formatted`, and `Exploitation` storage extend its functionality for specific tasks. The `Trusted` layer includes 
extensive data cleaning and transformation methods, the `Formatted` layer focuses on file handling, and the 
`Exploitation` layer enables data aggregation and joins for analysis. Specific data sources and formats, like CSV 
and JSON, have specialized classes under the `Formatted` layer, while `Trusted` classes manage detailed data 
operations for the different sources. 
"""
)
