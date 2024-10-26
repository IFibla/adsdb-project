import os
import re
import shutil


def classify_file(filename, patterns):
    for pattern, destination in patterns:
        match = re.match(pattern, filename)
        if match:
            date = match.group(1)
            new_filename = date + os.path.splitext(filename)[1]
            return new_filename, destination
    return None, None


def main(temporal_folder, persistent_folder):
    patterns = [
        (
            r"^Motor_Vehicle_Collisions_-_Crashes_(\d{8}).csv$",
            os.path.join(persistent_folder, "motor_vehicle_collisions", "crashes"),
        ),
        (
            r"^Motor_Vehicle_Collisions_-_Persons_(\d{8}).csv$",
            os.path.join(persistent_folder, "motor_vehicle_collisions", "person"),
        ),
        (
            r"^Motor_Vehicle_Collisions_-_Vehicles_(\d{8}).csv$",
            os.path.join(persistent_folder, "motor_vehicle_collisions", "vehicles"),
        ),
        (
            r"^NHTSA_-_Safety_Rating_(\d{8}).json$",
            os.path.join(persistent_folder, "nhtsa", "safety_rating"),
        ),
    ]

    for f in os.listdir(temporal_folder):
        new_filename, destination_folder = classify_file(f, patterns)

        if new_filename and destination_folder:
            os.makedirs(destination_folder, exist_ok=True)

            shutil.move(
                os.path.join(temporal_folder, f),
                os.path.join(destination_folder, new_filename),
            )


if __name__ == "__main__":
    main("/mnt/c/Users/ferran.gonzalez.gar/Documents/Repos/adsdb-project/data/landing/temporal/",
         "/mnt/c/Users/ferran.gonzalez.gar/Documents/Repos/adsdb-project/data/landing/persistent/")
