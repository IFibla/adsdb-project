import shutil
import os
import re


def classify_file(filename, patterns):
    """
    Classifies a file based on its filename by matching it with predefined patterns.
    Args:
        filename (str): The name of the file to classify.
        patterns (list[tuple]): A list of tuples, each containing a regex pattern and destination path.
    Returns:
        tuple: New filename and destination folder if a match is found; otherwise (None, None).
    """
    for pattern, destination in patterns:
        match = re.match(pattern, filename)
        if match:
            date = match.group(1)  # Extracts date from the matched pattern
            new_filename = (
                date + os.path.splitext(filename)[1]
            )  # Renames the file with extracted date
            return (
                new_filename,
                destination,
            )  # Returns new filename and destination folder
    return None, None  # Returns None if no match is found


def main(temporal_folder, persistent_folder):
    """
    Main function to classify and move files from a temporal folder to a persistent folder.
    Args:
        temporal_folder (str): The folder containing files to be processed.
        persistent_folder (str): The target folder where files will be organized and stored.
    """
    # Defines file patterns and target folders for classification
    patterns = [
        (
            r"^Motor_Vehicle_Collisions_-_Crashes_(\d{8}).csv$",
            os.path.join(persistent_folder, "motor_vehicle_collisions", "crashes"),
        ),
        (
            r"^Motor_Vehicle_Collisions_-_Person_(\d{8}).csv$",
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

    for f in os.listdir(temporal_folder):  # Iterates over files in the temporal folder
        new_filename, destination_folder = classify_file(
            f, patterns
        )  # Classifies each file

        if new_filename and destination_folder:
            os.makedirs(
                destination_folder, exist_ok=True
            )  # Creates the destination folder if it doesn't exist
            shutil.move(
                os.path.join(temporal_folder, f),
                os.path.join(destination_folder, new_filename),
            )  # Moves the file to the designated location


if __name__ == "__main__":
    main(
        temporal_folder="path_to_temporal_folder",
        persistent_folder="path_to_persistent_folder",
    )
