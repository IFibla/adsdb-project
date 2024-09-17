from abc import ABC, abstractmethod
from typing import Any


class Datasource(ABC):
    """
    Abstract base class for data sources.

    The `Datasource` class serves as a blueprint for all data source implementations.
    It enforces a consistent interface for retrieving data across different data sources
    by defining the abstract method `get`. All subclasses of `Datasource` must implement
    the `get` method to fetch data according to their specific data retrieval logic.

    Methods
    -------
    get():
        Abstract method to be implemented by subclasses for retrieving data.
    """

    @abstractmethod
    def get(self) -> Any:
        """
        Retrieve data from the data source.

        This method must be implemented by any subclass of `Datasource`. The implementation
        should define the specific way in which data is fetched from the data source.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.

        Returns
        -------
        Any
            The data retrieved from the data source, the format of which is defined by the
            implementing subclass.
        """
        pass
