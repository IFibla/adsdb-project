from models.ingestion.datasource import Datasource


class CSVDatasource(Datasource):
    """
    CSV Data Source Implementation of the Datasource Abstract Base Class.

    The `CSVDatasource` class implements the abstract `Datasource` class for CSV file data sources.
    It initializes with a specified file path and provides a method to retrieve the data
    stored in the CSV file.

    Parameters
    ----------
    i_filepath : str
        The file path to the CSV file from which data will be read.

    Methods
    -------
    get() -> bytes:
        Reads and returns the contents of the CSV file as bytes.
    """

    def __init__(self, i_filepath: str):
        """
        Initializes the CSVDatasource with the specified file path.

        Parameters
        ----------
        i_filepath : str
            The file path to the CSV file.
        """
        self.m_filepath = i_filepath

    def get(self) -> bytes:
        """
        Retrieve data from the CSV file.

        This method reads the content of the CSV file specified during initialization and
        returns it as bytes.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.

        Returns
        -------
        bytes
            The contents of the CSV file in bytes format.
        """
        with open(self.m_filepath, "rb") as o_file:
            return o_file.read()
