import os
from abc import abstractmethod

import pandas as pd

from models.storage.layer import Layer
from src.helpers.db_connector import DBConnector


class Formatted(Layer):

    def __init__(self, persistent_folder, formatted_db_connector: DBConnector):
        self.persistent_folder = persistent_folder
        self.formatted_db_connector = formatted_db_connector
        self.listed_files = self._list_files()

    @abstractmethod
    def _list_files(self) -> list[str]:
        pass


    @abstractmethod
    def _read_file(self, path : str) -> pd.DataFrame:
        pass

    def execute(self):
        for f in self.listed_files:
            formatted_table_name = f.replace('/', '_')
            if not self.formatted_db_connector.exists_table(formatted_table_name):
                df = self._read_file(f)
                self.formatted_db_connector.insert_data(formatted_table_name, df)
