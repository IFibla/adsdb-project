from abc import ABC, abstractmethod

from pandas import DataFrame


class Layer(ABC):
    """
    Abstract base class representing a data layer in a data ingestion pipeline.

    This class serves as a blueprint for creating specific types of layers that interact with data sources.
    It defines the structure and behavior that all derived layers must implement.

    Methods:
        get() -> DataFrame:
            Abstract method to retrieve data from the layer and return it as a pandas DataFrame.
            Must be implemented by subclasses.

    Raises:
        NotImplementedError: If the `get` method is not implemented in a derived class.
    """

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
