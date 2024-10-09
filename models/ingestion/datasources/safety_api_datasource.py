import requests

from models.ingestion.datasource import Datasource


class SafetyAPIDatasource(Datasource):
    """
    Concrete class for data retrieval from the NHTSA Safety Ratings API.

    The `SafetyAPIDatasource` class implements the Datasource interface to fetch data
    from the NHTSA Safety Ratings API endpoint. The class is responsible solely for
    making requests to the API and retrieving the raw data.
    """

    def __init__(self):
        """
        Initialize the SafetyAPIDatasource with the predefined API URL.
        """
        self.api_url = "https://api.nhtsa.gov/SafetyRatings/VehicleId"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def get(self, vehicle_id: int = 1) -> dict:
        """
        Fetch detailed data for a specific vehicle by its ID.

        This method implements the abstract `get` method from the Datasource class.
        It is used to make a request to the NHTSA API for a particular vehicle.

        Parameters
        ----------
        vehicle_id : int, optional
            The ID of the vehicle for which data is to be fetched. Defaults to 1.

        Returns
        -------
        dict
            A dictionary containing the response data from the API.
        """
        vehicle_url = f"{self.api_url}/{vehicle_id}"
        response = requests.get(vehicle_url, headers=self.headers)
        response.raise_for_status()
        return response.json()
