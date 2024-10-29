import streamlit as st

st.title("Landing")

st.markdown(
    """
This layer automates the organization of data files by moving them from a temporary directory to a 
structured, persistent storage location. The script uses a function classify_file that uses regular expressions to match 
filenames against predefined patterns, extracting dates from the filenames and determining the appropriate destination 
directories.

It iterates over all files in the temporal folder, classifies them using `classify_file`, and moves 
them to the correct locations after ensuring the destination directories exist. The script handles specific file types 
related to motor vehicle collisions and safety ratings, organizing them into subdirectories like "crashes", "person", 
"vehicles", and "safety_rating".

In our case, the resulted folder structure is:
```
├── persistent
│       ├── motor_vehicle_collisions
│       │       ├── crashes
│       │       │   ├── 20241026.csv
│       │       │   └── 20241026.csv
│       │       ├── person
│       │       │   ├── 20241026.csv
│       │       │   └── 20241027.csv
│       │       └── vehicles
│       │           ├── 20241026.csv
│       │           └── 20241027.csv
│       └── nhtsa
│           └── safety_rating
│               ├── 20241026.json
│               └── 20241027.json
└── temporal
    ├── motor_vehicle_collisions_crashes_20241028.csv
    ├── motor_vehicle_collisions_person_20241028.csv
    ├── motor_vehicle_collisions_vehicles_20241028.csv
    └── nhtsa_safety_rating_20241028.csv
```
"""
)
