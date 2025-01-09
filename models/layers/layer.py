from abc import ABC, abstractmethod

from pandas import DataFrame


class Layer(ABC):
    """
    Abstract base class representing a data layer in a data ingestion pipeline.
    This class serves as a blueprint for creating specific types of storage that interact with data sources.
    """

    @abstractmethod
    def execute(self):
        """
        Abstract method to execute actions associated with the layer.
        This method must be implemented in subclasses to perform data-related operations.
        Raises:
            NotImplementedError: If this method is not overridden in a derived class.
        """
        pass
