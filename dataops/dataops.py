import os

import requests
from tqdm import tqdm

from src.helpers.log_connector import LogDBConnector
from src.helpers.monitor import Monitoring
from .pipeline import Pipeline


class DataOps:
    def __init__(
        self,
        temporal_folder: str = r"data\landing\temporal",
        persistent_folder: str = r"data\landing\persistent",
        connector_folder: str = r"data",
    ):
        self._monitoring = Monitoring(interval=5)
        self.temporal_folder = os.path.abspath(temporal_folder)
        self.persistent_folder = os.path.abspath(persistent_folder)
        self.connector_folder = os.path.abspath(connector_folder)

        # Initialize the pipeline
        self.pipeline = Pipeline(
            temporal_folder=self.temporal_folder,
            persistent_folder=self.persistent_folder,
            connector_folder=self.connector_folder,
        )

        # Initialize the LogDBConnector
        self.log_connector = LogDBConnector(db_path="execution_log.db")
        self.log_connector.create_execution_log_table()

    def execute_pipeline(self):
        """
        Executes the entire pipeline.
        """
        print("Starting full pipeline execution...")
        self.pipeline.execute_all_stages()
        print("Full pipeline execution completed.")

    def execute_stage(self, stage_name: str):
        """
        Executes a specific stage of the pipeline.
        """
        print(f"Starting execution of stage: {stage_name}")
        self.pipeline.execute_stage(stage_name)
        print(f"Execution of stage '{stage_name}' completed.")

    def get_execution_logs(self):
        """
        Retrieves execution logs for all storage.
        """
        logs = self.log_connector.get_all_layer_statuses()
        if logs:
            print("Execution Logs:")
            for log in logs:
                layer_name, status, last_execution, error_message = log
                print(
                    f"Layer: {layer_name}, Status: {status}, Last Execution: {last_execution}, Error: {error_message}"
                )
        else:
            print("No execution logs found.")
        return logs

    def download_last_datasources(self):
        """
        Downloads the last data sources to the temporal folder.
        """
        urls = [
            "https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?date=20241030&accessType=DOWNLOAD",
            "https://data.cityofnewyork.us/api/views/bm4k-52h4/rows.csv?date=20241030&accessType=DOWNLOAD",
            "https://data.cityofnewyork.us/api/views/f55k-p6yu/rows.csv?date=20241030&accessType=DOWNLOAD",
        ]

        os.makedirs(self.temporal_folder, exist_ok=True)

        self._monitoring.start_monitoring()

        for url in urls:
            try:
                print(f"Starting download from {url}...")
                response = requests.get(url, stream=True)
                response.raise_for_status()

                content_disposition = response.headers.get("Content-Disposition")
                if content_disposition:
                    file_name = content_disposition.split("filename=")[-1].strip('";')
                else:
                    file_name = url.split("/")[-2] + ".csv"

                file_path = os.path.join(self.temporal_folder, file_name)
                total_size = int(response.headers.get("content-length", 0))

                with open(file_path, "wb") as file, tqdm(
                    desc=file_name,
                    total=total_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                        progress_bar.update(len(chunk))

                print(f"Downloaded and saved as {file_name} in {self.temporal_folder}")
            except requests.RequestException as e:
                print(f"Failed to download from {url}: {e}")

        self._monitoring.stop_monitoring()
