from src.helpers.data_profiler import DataProfiler
from src.helpers.db_connector import DBConnector
from models.layers.layer import Layer
from abc import abstractmethod
import pandas as pd
import os


class Formatted(Layer):
    """
    A class for formatting and storing data files in a structured database format.
    Inherits from Layer and handles files within a specified directory.
    """

    def __init__(self, persistent_folder, formatted_db_connector: DBConnector):
        """
        Initializes Formatted with a persistent folder path and database connector.
        Args:
            persistent_folder (str): Directory path where data files are stored.
            formatted_db_connector (DBConnector): Connector to the formatted database.
        """
        self.persistent_folder = persistent_folder
        self.formatted_db_connector = formatted_db_connector
        self.listed_files = self._list_files()  # List of files to process

    def _list_files(self) -> list[str]:
        """
        Lists all files in the persistent folder, returning their relative paths.
        Returns:
            list[str]: A list of file paths within the persistent folder.
        """
        file_paths = []
        for root, _, files in os.walk(self.persistent_folder):
            for file in files:
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, self.persistent_folder)
                file_paths.append(relative_path)
        return file_paths

    @abstractmethod
    def _read_file(self, path: str) -> pd.DataFrame:
        """
        Abstract method to read a data file at a specified path.
        Returns:
            pd.DataFrame: Data read from the file.
        """
        pass

    def compute_table_name(self, filename: str) -> str:
        """
        Computes a database-compatible table name based on the file path.
        Args:
            filename (str): Original file path.
        Returns:
            str: Formatted table name.
        """
        return filename.replace(os.path.sep, "_").replace("-", "")

    def execute(self):
        """
        Executes the process of reading and storing files as tables in the database.
        """
        for f in self.listed_files:
            formatted_table_name = self.compute_table_name(f)

            if not self.formatted_db_connector.exists_table(formatted_table_name):
                df = self._read_file(f)
                self.formatted_db_connector.insert_data(
                    formatted_table_name, df
                )  # Stores data
                print(f"Table {formatted_table_name} created successfully.")

    def get_profiling(self, table_name: str, export_path: str):
        """
        Generates a profiling report for a specified table.
        Args:
            table_name (str): Name of the table to profile.
            export_path (str): Path where the profiling report will be saved.
        """
        df = self.formatted_db_connector.read_data(table_name)
        profile = DataProfiler(df)
        profile.generate_report(export_path)
