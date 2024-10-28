from src.helpers.db_connector import DBConnector
from ydata_profiling import ProfileReport
from models.storage.layer import Layer
from abc import abstractmethod

import pandas as pd


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

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def _drop_insignificant_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def execute(self):
        from datetime import datetime

        print(f"{datetime.now()}: Starting")
        tables_names = self._list_tables()
        print(f"{datetime.now()}: Completed _list_tables")

        df = self._join_all_versions(tables_names)
        print(f"{datetime.now()}: Completed _join_all_versions")

        df = self._transform_column_names_to_snake_case(df)
        print(f"{datetime.now()}: Completed _transform_column_names_to_snake_case")

        df = self._drop_insignificant_columns(df)
        print(f"{datetime.now()}: Completed _drop_insignificant_columns")

        df = self._clean_duplicates(df)
        print(f"{datetime.now()}: Completed _clean_duplicates")

        df = self._correct_misspellings(df)
        print(f"{datetime.now()}: Completed _correct_misspellings")

        df = self._format_data(df)
        print(f"{datetime.now()}: Completed _format_data")

        df = self._handle_missing_values(df)
        print(f"{datetime.now()}: Completed _handle_missing_values")

        self.trusted_db_connector.insert_data(self._get_trusted_table_name(), df)
        print(f"{datetime.now()}: Data inserted into {self._get_trusted_table_name()}")

        print(f"Table {self._get_trusted_table_name()} created successfully.")

    def get_profiling(self, export_path: str):
        df = self.formatted_db_connector.get_table_as_dataframe(
            self._get_trusted_table_name()
        )
        ProfileReport(
            df, title=f"Profile Report from {self._get_trusted_table_name()}"
        ).to_file(export_path, silent=True)
