import re

from models.storage.layers.trusted import Trusted
import pandas as pd


class MVCCrash(Trusted):
    def _get_trusted_table_name(self) -> str:
        return "mvc_crash"

    def _list_tables(self) -> list[str]:
        return list(filter)

    def _transform_column_names_to_snake_case(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [
            re.sub(r"(?<!^)(?=[A-Z])", "_", col).lower() for col in df.columns
        ]
        return df

    def join_all_versions(self, tables_names: list[str]) -> pd.DataFrame:
        dfs = []
        for table_name in tables_names:
            dfs.append(
                self.formatted_db_connector.execute_query(
                    f"""SELECT * FROM {table_name}"""
                )
            )
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
