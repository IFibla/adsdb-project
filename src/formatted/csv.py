import os

import pandas as pd

from models.storage.layers.formatted import Formatted
from src.helpers.db_connector import DBConnector


class CSVFormatted(Formatted):

    def _list_files(self) -> list[str]:
        return [
            os.path.join(self.persistent_folder, f)
            for f in os.walk(self.persistent_folder)
            if f.endswith('.csv')
        ]

    def _read_file(self, path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(path)
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    persistent_folder = "/mnt/c/Users/ferran.gonzalez.gar/Documents/Repos/adsdb-project/data/landing/persistent/"
    formatted_db_connector = DBConnector()
    csv_formatter = CSVFormatted(persistent_folder, formatted_db_connector)

    print("Listed CSV files:")
    for file in csv_formatter.listed_files:
        print(file)

    # Test reading each file
    for file in csv_formatter.listed_files:
        df = csv_formatter._read_file(file)
        print(f"Data from {file}:")
        print(df.head())