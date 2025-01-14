import streamlit as st
import pandas as pd

st.title("Datasources")
st.write("## New York City Open Data")

st.markdown(
    """
The Motor Vehicle Collisions data tables provide comprehensive information on all police-reported motor vehicle collisions in New York City. These tables include:

- **Crash Table**: Contains detailed information on each crash event, with each row representing a single incident.
- **Person Table**: Provides details for every person involved in a crash, including drivers, occupants, pedestrians, and bicyclists. Each row represents an individual involved in a collision. Data available from April 2016 onwards.
- **Vehicle Table**: Contains information on each vehicle involved in a crash, with each row representing a single vehicle. Data available from April 2016 onwards.
"""
)
with st.expander("Motor Vehicle Collisions Crash"):
    st.link_button(
        "Download",
        "https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data",
    )
    st.dataframe(
        pd.read_csv(
            "./data/landing/persistent/motor_vehicle_collisions/crashes/2023.csv",
            nrows=10,
        )
    )

with st.expander("Motor Vehicle Collisions Person"):
    st.link_button(
        "Download",
        "https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu/about_data",
    )
    st.dataframe(
        pd.read_csv(
            "data/landing/persistent/motor_vehicle_collisions/person/2023.csv",
            nrows=10,
        )
    )

with st.expander("Motor Vehicle Collisions Vehicle"):
    st.link_button(
        "Download",
        "https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4/about_data",
    )
    st.dataframe(
        pd.read_csv(
            "data/landing/persistent/motor_vehicle_collisions/vehicles/2023.csv",
            nrows=10,
        )
    )

st.write("## National Highway Traffic Safety Administration")
st.markdown(
    """
The NHTSA Safety Ratings provide consumers with comprehensive information on the crash protection and rollover safety of new vehicles. The ratings help consumers make informed decisions when purchasing a vehicle by comparing safety features and performance.

**The ratings include:**

- **Frontal Crash Ratings**: Assess the vehicle's performance in head-on collisions, with separate ratings for the driver and front passenger.
- **Side Crash Ratings**: Evaluate the vehicle's performance in side-impact collisions, including side barrier and side pole tests.
- **Rollover Ratings**: Estimate the vehicle's risk of rollover in a single-vehicle loss-of-control scenario.

Vehicles are rated on a scale from one to five stars, with five stars indicating the highest level of safety.
"""
)


def fetch_vehicle_data(vehicle_id: int) -> dict:
    import requests

    api_url = "https://api.nhtsa.gov/SafetyRatings/VehicleId"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }
    try:
        response = requests.get(f"{api_url}/{vehicle_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data for vehicle ID {vehicle_id}: {e}")
        return {}


with st.expander("Vehicle Safety Rating"):
    number = st.number_input(
        "Insert the vehicle ID",
        min_value=1,
        max_value=25000,
    )

    st.json(fetch_vehicle_data(number))
