from src.helpers.db_connector import (
    DBConnector,
)
from models.layers.layer import Layer
from abc import abstractmethod
import pandas as pd


class AnalyticalSandbox(Layer):
    """
    A base class for analytical sandbox processes that extends the Layer class.
    This class is designed to manage and execute data extraction and filtering from the
    exploitation database to the analytical sandbox database.
    """

    def __init__(
        self,
        exploitation_db_connector: DBConnector,
        analytical_sandbox_db_connector: DBConnector,
    ):
        """
        Initializes AnalyticalSandbox with connectors for both exploitation and
        analytical sandbox databases.

        Args:
            exploitation_db_connector (DBConnector): Connector for the exploitation database.
            analytical_sandbox_db_connector (DBConnector): Connector for the analytical sandbox database.
        """
        self.exploitation_db_connector = exploitation_db_connector
        self.analytical_sandbox_db_connector = analytical_sandbox_db_connector

    @abstractmethod
    def _get_exploitation_table_name(self) -> str:
        """
        Abstract method to define the source table name from the exploitation database.

        Returns:
            str: The name of the table in the exploitation database.
        """
        pass

    @abstractmethod
    def _get_analytical_sandbox_table_name(self) -> str:
        """
        Abstract method to define the target table name in the analytical sandbox database.

        Returns:
            str: The name of the table in the analytical sandbox database.
        """
        pass

    @abstractmethod
    def _filter_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method to filter the extracted DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to be filtered.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        return df

    def execute(self):
        """
        Executes the data extraction, filtering, and loading process.
        Extracts data from the exploitation database, applies filtering, and
        loads the result into the analytical sandbox database.
        """
        df = self.exploitation_db_connector.get_table_as_dataframe(
            self._get_exploitation_table_name()
        )
        df = self._filter_dataframe(df)
        self.analytical_sandbox_db_connector.insert_data(
            self._get_analytical_sandbox_table_name(), df
        )
        print(
            f"Table {self._get_analytical_sandbox_table_name()} created successfully."
        )
