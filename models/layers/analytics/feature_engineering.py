import os

from sklearn.model_selection import train_test_split

from src.analytics.models.car_make import CarMakeEmbedding
from src.helpers.db_connector import (
    DBConnector,
)
from models.layers.layer import Layer
from abc import abstractmethod
import pandas as pd


class FeatureEngineering(Layer):
    """
    A base class for feature engineering processes that extends the Layer class.
    This class is designed to manage and execute data transformation and loading from the
    analytical sandbox database to the feature engineering database.
    """

    cme = CarMakeEmbedding(
        label_encoder=r'data/models/encoder.pkl',
        pkl_path=r'data/models/embedding.pkl',
    )

    def __init__(
        self,
        analytical_sandbox_db_connector: DBConnector,
        feature_engineering_db_connector: DBConnector,
    ):
        """
        Initializes FeatureEngineering with connectors for both the analytical sandbox and
        feature engineering databases.

        Args:
            analytical_sandbox_db_connector (DBConnector): Connector for the analytical sandbox database.
            feature_engineering_db_connector (DBConnector): Connector for the feature engineering database.
        """
        self.analytical_sandbox_db_connector = analytical_sandbox_db_connector
        self.feature_engineering_db_connector = feature_engineering_db_connector

    @abstractmethod
    def _get_analytical_sandbox_table_name(self) -> str:
        """
        Abstract method to define the source table name from the analytical sandbox database.

        Returns:
            str: The name of the table in the analytical sandbox database.
        """
        pass

    @abstractmethod
    def _get_feature_engineering_table_name(self) -> str:
        """
        Abstract method to define the target table name in the feature engineering database.

        Returns:
            str: The name of the table in the feature engineering database.
        """
        pass

    @abstractmethod
    def _transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method to transform the extracted DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to be transformed.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """
        pass


    def execute(self):
        """
        Executes the data extraction, transformation, and loading process.
        Extracts data from the analytical sandbox database, applies transformations, and
        loads the result into the feature engineering database.
        """
        df = self.analytical_sandbox_db_connector.get_table_as_dataframe(
            self._get_analytical_sandbox_table_name()
        )
        df = self._transform_dataframe(df)

        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

        self.feature_engineering_db_connector.insert_data(
            f"{self._get_feature_engineering_table_name()}_train", train_df
        )

        print(
            f"Table {self._get_feature_engineering_table_name()}_train created successfully."
        )

        self.feature_engineering_db_connector.insert_data(
            f"{self._get_feature_engineering_table_name()}_test", test_df
        )

        print(
            f"Table {self._get_feature_engineering_table_name()}_test created successfully."
        )
