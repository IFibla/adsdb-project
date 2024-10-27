from src.helpers.db_connector import DBConnector
from ydata_profiling import ProfileReport
from models.storage.layer import Layer
from abc import abstractmethod
import pandas as pd
import os


class Formatted(Layer):
    def __init__(self, persistent_folder, formatted_db_connector: DBConnector):
        self.persistent_folder = persistent_folder
        self.formatted_db_connector = formatted_db_connector
        self.listed_files = self._list_files()

    def _list_files(self) -> list[str]:
        file_paths = []
        for root, _, files in os.walk(self.persistent_folder):
            for file in files:
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, self.persistent_folder)
                file_paths.append(relative_path)
        return file_paths

    @abstractmethod
    def _read_file(self, path: str) -> pd.DataFrame:
        pass

    def compute_table_name(self, filename: str) -> str:
        return filename.replace(os.path.sep, "_").replace("-", "")

    def execute(self):
        for f in self.listed_files:
            formatted_table_name = self.compute_table_name(f)

            if not self.formatted_db_connector.exists_table(formatted_table_name):
                df = self._read_file(f)
                self.formatted_db_connector.insert_data(formatted_table_name, df)

    def get_profiling(self, table_name: str, export_path: str):
        df = self.formatted_db_connector.get_table_as_dataframe(table_name)
        ProfileReport(df, title=f"Profile Report from {table_name}").to_file(
            export_path, silent=True
        )
