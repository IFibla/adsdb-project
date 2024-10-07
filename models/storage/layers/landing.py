from models.ingestion.datasource import Datasource
from models.storage.layer import Layer
from abc import abstractmethod
from pandas import DataFrame


class Landing(Layer):
    """
    Abstract class representing a landing layer in a data ingestion pipeline.

    The Landing class extends the Layer class, specifically designed for handling
    data sourced from various data ingestion sources. It defines the necessary
    structure for retrieving data from a datasource in a landing zone context.

    Attributes:
        m_datasource (Datasource): An instance of Datasource representing the data source
        associated with this landing layer.

    Methods:
        __init__(i_datasource: Datasource):
            Initializes the Landing instance with the specified datasource.

        get() -> DataFrame:
            Abstract method to retrieve data from the landing layer and return it as a pandas DataFrame.
            Must be implemented by subclasses.

    Raises:
        NotImplementedError: If the `get` method is not implemented in a derived class.
    """

    @abstractmethod
    def __init__(self, i_datasource: Datasource):
        """
        Initializes the Landing instance.

        Args:
            i_datasource (Datasource): An instance of Datasource that this landing layer will use
            to retrieve data.
        """
        pass

    @abstractmethod
    def get(self) -> DataFrame:
        """
        Abstract method to retrieve data from the landing layer.

        This method must be implemented in subclasses to return data as a pandas DataFrame.

        Returns:
            DataFrame: The data retrieved from the landing layer.

        Raises:
            NotImplementedError: If this method is not overridden in a derived class.
        """
        pass
