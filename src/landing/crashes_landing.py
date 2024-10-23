import pandas as pd
from pandas import DataFrame

from models.storage.layers.landing import Landing
from datetime import datetime
import shutil
import json
import os
import re


class CrashesLanding(Landing):
    """
    Concrete class representing a safety data landing layer in a data ingestion pipeline.

    The CrashesLanding class is specifically designed to retrieve CSV data from a temporary landing zone
    and store it in a persistent landing zone, along with its metadata.

    Attributes:
        m_temporal_landing_path (str): Path to the temporary landing zone where incoming CSV files are stored.
        m_persistent_landing_path (str): Path to the persistent landing zone where processed files are stored.
    """

    def __init__(
        self,
        i_temporal_landing_path: str,
        i_persistent_landing_path: str,
        i_filename: str,
    ):
        """
        Initializes the CrashesLanding instance with specified paths for temporal and persistent landing zones.

        Args:
            i_temporal_landing_path (str): The path for the temporary landing zone.
            i_persistent_landing_path (str): The path for the persistent landing zone.
        """
        self.m_temporal_landing_path = i_temporal_landing_path
        self.m_persistent_landing_path = i_persistent_landing_path
        self.m_filename = i_filename
        if not os.path.exists(self.m_temporal_landing_path + self.m_filename):
            raise FileNotFoundError(
                f"{self.m_temporal_landing_path}{self.m_filename} was not found."
            )

        dates = re.findall(r"\d{8}", self.m_filename)

        if len(dates) != 1:
            raise ValueError(f"{self.m_filename} has 0 or >1 dates.")

        try:
            self.m_date_obj = datetime.strptime(dates[0], "%Y%m%d")
        except ValueError as e:
            print(f"Error parsing date '{dates[0]}': {e}")
            return

        self.m_persistent_folder = self.m_date_obj.strftime("%Y%m%d") + "/"

    def execute(self):
        """
        Retrieves and processes a CSV file from the temporary landing zone, then saves it in the persistent landing zone.

        This method checks if the specified CSV file exists in the temporary landing path, extracts the date from the
        filename, and creates a corresponding directory in the persistent landing path to save the file and its metadata.

        Raises:
            FileNotFoundError: If the specified file does not exist in the temporal landing path.
            ValueError: If the filename contains zero or more than one date.
            ValueError: If the date extracted from the filename cannot be parsed.

        Returns:
            None: The method saves the CSV file and its metadata in the persistent landing zone.
        """
        os.makedirs(
            f"{self.m_persistent_landing_path}{self.m_persistent_folder}", exist_ok=False
        )
        shutil.copyfile(
            self.m_temporal_landing_path + self.m_filename,
            self.m_persistent_landing_path + self.m_persistent_folder + "Crashes.csv",
        )

        metadata = {
            "temporal_landing_path": f"{self.m_temporal_landing_path}{self.m_filename}",
            "persistent_landing_path": f"{self.m_persistent_landing_path}{self.m_persistent_folder}",
            "data_provider": "Police Department (NYPD)",
            "dataset_owner": "NYC OpenData",
            "data_collection": "Motor Vehicle Collisions",
            "agency": "Police Department (NYPD)",
            "update_frequency": "Daily",
            "date": self.m_date_obj.strftime("%Y%m%d")
        }

        with open(
            self.m_persistent_landing_path + self.m_persistent_folder + "Crashes.metadata", "w"
        ) as f:
            f.write(json.dumps(metadata))

    def get(self) -> DataFrame:
        df = pd.read_csv(f'{self.m_persistent_landing_path}{self.m_persistent_folder}/Crashes.csv')
        with open(f'{self.m_persistent_landing_path}{self.m_persistent_folder}/Crashes.metadata', 'r') as file:
            metadata = json.loads(file.read())
        for key, value in metadata.items():
            df[f'metadata_{key}'] = value
        return df