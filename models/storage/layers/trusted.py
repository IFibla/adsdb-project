from abc import abstractmethod

import pandas as pd

from models.storage.layer import Layer
from src.helpers.db_connector import DBConnector


class Trusted(Layer):
    def __init__(
        self,
        formatted_db_connector: DBConnector,
        trusted_db_connector: DBConnector,
    ):
        self.formatted_db_connector = formatted_db_connector
        self.trusted_db_connector = trusted_db_connector

    @abstractmethod
    def _get_trusted_table_name(self) -> str:
        pass

    def _list_tables(self) -> list[str]:
        return self.formatted_db_connector.get_tables()

    def _transform_column_names_to_snake_case(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.replace(" ", "_").lower() for col in df.columns]
        return df

    def _join_all_versions(self, tables_names: list[str]) -> pd.DataFrame:
        dfs = []
        for table_name in tables_names:
            dfs.append(self.formatted_db_connector.get_table_as_dataframe(table_name))
        return pd.concat(dfs, axis=0, ignore_index=True)

    def _clean_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def _correct_misspellings(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def _profile_data(self, df: pd.DataFrame) -> dict:
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def _drop_insignificant_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def execute(self):
        tables_names = self._list_tables()
        df = self._join_all_versions(tables_names)
        df = self._transform_column_names_to_snake_case(df)
        df = self._drop_insignificant_columns(df)
        df = self._clean_duplicates(df)
        df = self._correct_misspellings(df)
        df = self._format_data(df)
        df = self._handle_missing_values(df)
        self.trusted_db_connector.insert_data(self._get_trusted_table_name(), df)
