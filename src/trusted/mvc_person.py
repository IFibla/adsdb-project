from models.storage.layers.trusted import Trusted
import pandas as pd


class MVCPerson(Trusted):
    def _get_trusted_table_name(self) -> str:
        return "mvc_person"

    def _list_tables(self) -> list[str]:
        pass

    def _transform_column_names_to_snake_case(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def join_all_versions(self, tables_names: list[str]) -> pd.DataFrame:
        pass

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
