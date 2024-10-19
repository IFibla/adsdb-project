from abc import abstractmethod
from typing import Any

from pandas import DataFrame

from models.storage.layer import Layer
from models.storage.layers.landing import Landing
from src.helpers.db_connector import DBConnector


class Formatted(Layer):
    """
    Abstract class representing a formatted layer in a data ingestion pipeline.

    The Formatted class extends the Layer class and provides the basic structure for transforming
    or formatting data from various data sources or other layers into a consistent format.

    Attributes:
        m_landing (Landing): An instance of a Landing that provides the raw data to be formatted.

    Methods:
        format_data(data: Any) -> DataFrame:
            Abstract method to transform raw data from its original format into a standardized pandas DataFrame.
            This must be implemented by subclasses.

        get() -> DataFrame:
            Retrieves and formats data from the source layer.
    """

    def __init__(self, i_landing: Landing, i_db_connector: DBConnector):
        self.m_landing = i_landing
        self.m_db_connector = i_db_connector

    @abstractmethod
    def format_data(self, data: Any) -> DataFrame:
        """
                Abstract method to transform raw data from its original format into a standardized pandas DataFrame.

                This method must be implemented by subclasses to provide the specific transformation logic
                needed to standardize the data format.
        ç
                Args:
                    data (Any): The raw data retrieved from the source layer, which could be in various formats
                    (e.g., dict, bytearray, etc.).

                Returns:
                    DataFrame: The standardized data as a pandas DataFrame.
        """
        pass

    def get(self) -> DataFrame:
        raw_data = self.m_landing.get()
        return self.format_data(raw_data)
