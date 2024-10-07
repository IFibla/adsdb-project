import requests

from ..datasource import Datasource


class APIDatasource(Datasource):
    """
    Concrete class for data retrieval from an API.

    The `APIDatasource` class implements the `Datasource` interface to fetch data
    from an external API. The `get` method sends a request to the specified API
    endpoint and returns the response data.

    Attributes
    ----------
    api_url : str
        The base URL of the API endpoint.
    headers : dict, optional
        Headers to be sent with the API request, such as authorization tokens.
    params : dict, optional
        Query parameters to be included in the request.
    """

    def __init__(self, api_url: str, headers: dict = None, params: dict = None):
        """
        Initialize the APIDatasource with the API URL and optional headers and parameters.

        Parameters
        ----------
        api_url : str
            The URL of the API from which to retrieve data.
        headers : dict, optional
            HTTP headers to include in the request, such as authentication tokens.
        params : dict, optional
            Query parameters to include in the request.
        """
        self.api_url = api_url
        self.headers = headers if headers else {}
        self.params = params if params else {}

    def get(self) -> any:
        """
        Fetch data from the API.

        This method sends a GET request to the specified API URL with optional
        headers and query parameters. If the request is successful, it returns
        the response data.

        Raises
        ------
        Exception
            If the API request fails.

        Returns
        -------
        Any
            The data retrieved from the API, typically in JSON format.
        """
        try:
            response = requests.get(self.api_url, headers=self.headers, params=self.params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch data from API: {e}")
