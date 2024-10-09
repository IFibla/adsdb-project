from models.ingestion.datasource import Datasource
from abc import ABC, abstractmethod
from pandas import DataFrame
from typing import Self


class Layer(ABC):
    """
    Abstract base class representing a data layer in a data ingestion pipeline.

    This class serves as a blueprint for creating specific types of layers that interact with data sources.
    It defines the structure and behavior that all derived layers must implement.

    Attributes:
        m_source (Datasource | Self | [Self]): An instance of a Datasource, another Layer instance, or a list of Layer instances
        that this layer interacts with.

    Methods:
        __init__(i_source: Datasource | Self | [Self]):
            Initializes the layer with a specified data source or layer.

        get() -> DataFrame:
            Abstract method to retrieve data from the layer and return it as a pandas DataFrame.
            Must be implemented by subclasses.

    Raises:
        NotImplementedError: If the `get` method is not implemented in a derived class.
    """

    def __init__(self, i_source: Datasource | Self | [Self]):
        """
        Initializes the Layer instance.

        Args:
            i_source (Datasource | Self | [Self]): An instance of Datasource, another Layer instance, or a list of Layer instances
            that this layer will use for data operations.

        """
        self.m_source = i_source

    @abstractmethod
    def get(self) -> DataFrame:
        """
        Abstract method to retrieve data from the layer.

        This method must be implemented in subclasses to return data as a pandas DataFrame.

        Returns:
            DataFrame: The data retrieved from the layer.

        Raises:
            NotImplementedError: If this method is not overridden in a derived class.
        """
        pass
