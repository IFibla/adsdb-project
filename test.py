from tqdm import tqdm
import pandas as pd

df_crash = pd.read_csv(
    "/Users/ignasi/Documents/_03_MDS_/_01_ADSDB_/data/landing/persistent/motor_vehicle_collisions/crashes/20241026.csv1",
    parse_dates=["CRASH DATE"],
)
df_person = pd.read_csv(
    "/Users/ignasi/Documents/_03_MDS_/_01_ADSDB_/data/landing/persistent/motor_vehicle_collisions/person/20241027.csv1",
    parse_dates=["CRASH_DATE"],
)
df_vehicle = pd.read_csv(
    "/Users/ignasi/Documents/_03_MDS_/_01_ADSDB_/data/landing/persistent/motor_vehicle_collisions/vehicles/20241027.csv1",
    parse_dates=["CRASH_DATE"],
)
df_crash["Year"] = df_crash["CRASH DATE"].dt.year
df_person["Year"] = df_person["CRASH_DATE"].dt.year
df_vehicle["Year"] = df_vehicle["CRASH_DATE"].dt.year

df_crash = df_crash[df_crash["Year"] == 2024]
df_person = df_person[df_person["Year"] == 2024]
df_vehicle = df_vehicle[df_vehicle["Year"] == 2024]

counter = 0
for year, data in tqdm(df_crash.groupby("CRASH DATE")):
    data.to_csv(
        f"/Users/ignasi/Documents/_03_MDS_/_01_ADSDB_/ui/simulation/landing/temporal/Motor_Vehicle_Collisions_-_Crashes_{year.strftime('%Y%m%d')}.csv",
        index=False,
    )
    counter += 1
    if counter == 5:
        break

counter = 0
for year, data in tqdm(df_person.groupby("CRASH_DATE")):
    data.to_csv(
        f"/Users/ignasi/Documents/_03_MDS_/_01_ADSDB_/ui/simulation/landing/temporal/Motor_Vehicle_Collisions_-_Person_{year.strftime('%Y%m%d')}.csv",
        index=False,
    )
    counter += 1
    if counter == 5:
        break

counter = 0
for year, data in tqdm(df_vehicle.groupby("CRASH_DATE")):
    data.to_csv(
        f"/Users/ignasi/Documents/_03_MDS_/_01_ADSDB_/ui/simulation/landing/temporal/Motor_Vehicle_Collisions_-_Vehicles_{year.strftime('%Y%m%d')}.csv",
        index=False,
    )
    counter += 1
    if counter == 5:
        break

import shutil

shutil.copy(
    "/Users/ignasi/Documents/_03_MDS_/_01_ADSDB_/data/landing/persistent/nhtsa/safety_rating/20241027.json",
    "/Users/ignasi/Documents/_03_MDS_/_01_ADSDB_/ui/simulation/landing/temporal/NHTSA_-_Safety_Rating_20241027.json",
)
