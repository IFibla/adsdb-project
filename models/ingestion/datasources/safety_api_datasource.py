import concurrent.futures
import logging

import requests

logging.basicConfig(level=logging.INFO)

from models.ingestion.datasource import Datasource


class SafetyAPIDatasource(Datasource):
    """
    Concrete class for data retrieval from a specific safety-related API.

    The SafetyAPIDatasource class implements the Datasource interface to fetch data
    from a designated safety-related API endpoint.

    Attributes
    ----------
    api_url : str
        The base URL of the safety-related API endpoint.
    """

    def __init__(self, debug_range: range = None, max_workers: int = 20):
        """
        Initialize the SafetyAPIDatasource with a predefined API URL.

        The URL is fixed for the safety API.
        """
        self.api_url = "https://api.nhtsa.gov/SafetyRatings/VehicleId"
        self.debug_range = debug_range if debug_range else range(1, 20001)
        self.max_workers = max_workers

    def get(self) -> list:
        """
        Fetch data for vehicle IDs ranging from 1 to 20000.

        This method sends GET requests for each vehicle ID from 1 to 20000 in parallel.
        It then returns the collected data for each vehicle.

        Raises
        ------
        Exception
            If any of the API requests fail.

        Returns
        -------
        list
            The combined results obtained from the additional API requests for each vehicle ID.
        """
        vehicle_details: list = []
        # Use ThreadPoolExecutor to make requests in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Create futures for each vehicle ID from 1 to 20000
            futures: dict = {executor.submit(self._get_vehicle_data, vehicle_id): vehicle_id for vehicle_id in self.debug_range}

            for future in concurrent.futures.as_completed(futures):
                vehicle_id = futures[future]
                try:
                    vehicle_data = future.result()
                    if vehicle_data and 'Results' in vehicle_data:
                        vehicle_details.extend(vehicle_data['Results'])
                except requests.exceptions.RequestException as e:
                    logging.warning(f"Failed to fetch data for vehicle ID {vehicle_id}: {e}")

        return vehicle_details

    def _get_vehicle_data(self, vehicle_id: int) -> dict[str, any]:
        """
        Fetch detailed data for a specific vehicle by its ID.

        Parameters
        ----------
        vehicle_id : int
            The ID of the vehicle for which data is to be fetched.

        Returns
        -------
        list
            The detailed data for the specified vehicle.
        """
        vehicle_url = f"{self.api_url}/{vehicle_id}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        try:
            response = requests.get(vehicle_url, headers=headers)
            response.raise_for_status()
            vehicle_data: dict = response.json()
            return vehicle_data
        except requests.exceptions.RequestException as e:
            logging.warning(f"Failed to retrieve data for vehicle ID {vehicle_id}: {e}")
            return {}