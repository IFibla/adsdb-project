from src.helpers.data_profiler import DataProfiler
from src.helpers.db_connector import DBConnector
from models.storage.layer import Layer
from abc import abstractmethod

import pandas as pd


class Trusted(Layer):
    """
    A class for managing trusted data transformations and storage, inheriting from the Layer base class.
    This class handles data cleaning, formatting, and joins across formatted data tables.
    """

    def __init__(
        self,
        formatted_db_connector: DBConnector,
        trusted_db_connector: DBConnector,
    ):
        """
        Initializes Trusted with connectors for formatted and trusted databases.
        Args:
            formatted_db_connector (DBConnector): Connector for the formatted database.
            trusted_db_connector (DBConnector): Connector for the trusted database.
        """
        self.formatted_db_connector = formatted_db_connector
        self.trusted_db_connector = trusted_db_connector

    @abstractmethod
    def _get_trusted_table_name(self) -> str:
        """
        Abstract method to get the table name for trusted data.
        """
        pass

    def _list_tables(self) -> list[str]:
        """
        Lists tables available in the formatted database.
        Returns:
            list[str]: A list of table names.
        """
        return self.formatted_db_connector.get_tables()

    def _transform_column_names_to_snake_case(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms column names in the DataFrame to snake_case.
        Args:
            df (pd.DataFrame): DataFrame with original column names.
        Returns:
            pd.DataFrame: DataFrame with column names in snake_case.
        """
        df.columns = [col.replace(" ", "_").lower() for col in df.columns]
        return df

    def _join_all_versions(self, tables_names: list[str]) -> pd.DataFrame:
        """
        Joins all versions of tables from the formatted database into a single DataFrame.
        Args:
            tables_names (list[str]): List of table names to join.
        Returns:
            pd.DataFrame: Combined DataFrame from all specified tables.
        """
        dfs = []
        for table_name in tables_names:
            dfs.append(self.formatted_db_connector.get_table_as_dataframe(table_name))
        return pd.concat(dfs, axis=0, ignore_index=True)

    def _clean_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder method for removing duplicates from a DataFrame.
        Returns:
            pd.DataFrame: DataFrame without duplicates.
        """
        return df

    def _correct_misspellings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder method for correcting misspellings in a DataFrame.
        Returns:
            pd.DataFrame: Corrected DataFrame.
        """
        return df

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder method for formatting data in a DataFrame.
        Returns:
            pd.DataFrame: Formatted DataFrame.
        """
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder method for handling missing values in a DataFrame.
        Returns:
            pd.DataFrame: DataFrame with handled missing values.
        """
        return df

    def _drop_insignificant_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder method for dropping insignificant columns from a DataFrame.
        Returns:
            pd.DataFrame: DataFrame with insignificant columns removed.
        """
        return df

    def execute(self):
        """
        Executes a sequence of data preparation steps on tables from the formatted database and
        saves the processed result to the trusted database.

        Steps:
            1. Lists available tables in the formatted database.
            2. Joins all versions of data tables into a single DataFrame.
            3. Transforms column names to snake_case for standardization.
            4. Drops insignificant columns from the DataFrame.
            5. Cleans duplicate records in the data.
            6. Corrects any known misspellings within the data.
            7. Formats data to ensure consistency across records.
            8. Handles missing values as per predefined rules.

        Finally, the processed DataFrame is saved to the trusted database under a specified table name.

        Raises:
            Any database connection or insertion errors.
        """
        tables_names = self._list_tables()
        df = self._join_all_versions(tables_names)
        df = self._transform_column_names_to_snake_case(df)
        df = self._drop_insignificant_columns(df)
        df = self._clean_duplicates(df)
        df = self._correct_misspellings(df)
        df = self._format_data(df)
        df = self._handle_missing_values(df)
        self.trusted_db_connector.insert_data(self._get_trusted_table_name(), df)
        print(f"Table {self._get_trusted_table_name()} created successfully.")

    def get_profiling(self, export_path: str):
        """
        Generates a data profiling report for the trusted database table and saves it to a specified path.

        Args:
            export_path (str): File path to export the generated profiling report.

        Steps:
            1. Retrieves the table data as a DataFrame from the formatted database.
            2. Creates a ProfileReport for data profiling, providing insights into the structure,
               distribution, and possible anomalies within the data.
            3. Exports the profiling report to the specified export path in HTML format.

        Raises:
            Any errors related to data retrieval or file export operations.
        """
        df = self.formatted_db_connector.get_table_as_dataframe(
            self._get_trusted_table_name()
        )
        profile = DataProfiler(df)
        profile.generate_report(export_path)
