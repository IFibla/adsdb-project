import os
import re
import shutil

from models.layers.layer import Layer


class Landing(Layer):
    def __init__(self, temporal_folder, persistent_folder):
        self.temporal_folder = temporal_folder
        self.persistent_folder = persistent_folder
        self.patterns = [
            (
                r"^Motor_Vehicle_Collisions_-_Crashes_(\d{8}).csv$",
                os.path.join(
                    self.persistent_folder, "motor_vehicle_collisions", "crashes"
                ),
            ),
            (
                r"^Motor_Vehicle_Collisions_-_Person_(\d{8}).csv$",
                os.path.join(
                    self.persistent_folder, "motor_vehicle_collisions", "person"
                ),
            ),
            (
                r"^Motor_Vehicle_Collisions_-_Vehicles_(\d{8}).csv$",
                os.path.join(
                    self.persistent_folder, "motor_vehicle_collisions", "vehicles"
                ),
            ),
            (
                r"^NHTSA_-_Safety_Rating_(\d{8}).json$",
                os.path.join(self.persistent_folder, "nhtsa", "safety_rating"),
            ),
        ]

    def classify_file(self, filename):
        for pattern, destination in self.patterns:
            match = re.match(pattern, filename)
            if match:
                date = match.group(1)
                new_filename = date + os.path.splitext(filename)[1]
                return new_filename, destination
        return None, None

    def execute(self):
        for f in os.listdir(self.temporal_folder):
            new_filename, destination_folder = self.classify_file(f)

            if new_filename and destination_folder:
                os.makedirs(destination_folder, exist_ok=True)
                shutil.move(
                    os.path.join(self.temporal_folder, f),
                    os.path.join(destination_folder, new_filename),
                )


if __name__ == "__main__":
    landing = Landing(
        temporal_folder=r"C:\Users\ferra\PycharmProjects\adsdb-project\data\landing\temporal",
        persistent_folder=r"C:\Users\ferra\PycharmProjects\adsdb-project\data\landing\persistent",
    )

    landing.execute()
