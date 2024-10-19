import concurrent.futures

import requests

from models.storage.layers.landing import Landing


class SafetyApiLanding(Landing):
    """
    Concrete class representing a safety API landing layer in a data ingestion pipeline.

    The SafetyApiLanding class is specifically designed to retrieve data from a safety-related API
    and return it in the form of JSON data.
    """

    def __init__(self, min_vehicle_id: int, max_vehicle_id: int):
        self.api_url = "https://api.nhtsa.gov/SafetyRatings/VehicleId"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        self.min_vehicle_id = min_vehicle_id
        self.max_vehicle_id = max_vehicle_id

    def _fetch_vehicle_data(self, vehicle_id: int) -> dict:
        try:
            response = requests.get(
                f"{self.api_url}/{vehicle_id}", headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data for vehicle ID {vehicle_id}: {e}")
            return {}

    def get(self) -> list:
        all_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {
                executor.submit(self._fetch_vehicle_data, vehicle_id): vehicle_id
                for vehicle_id in range(self.min_vehicle_id, self.max_vehicle_id + 1)
            }
            for future in concurrent.futures.as_completed(futures):
                all_results.append(future.result())

        return all_results
