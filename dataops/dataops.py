from dataops import Pipeline
from src.helpers.log_connector import LogDBConnector
from src.helpers.monitor import Monitoring


class DataOps:
    def __init__(
            self,
            temporal_folder: str = r"data\landing\temporal",
            persistent_folder: str = r"data\landing\persistent",
    ):
        self._monitoring = Monitoring(interval=5)
        self.temporal_folder = temporal_folder
        self.persistent_folder = persistent_folder

        # Initialize the pipeline
        self.pipeline = Pipeline(
            temporal_folder=self.temporal_folder,
            persistent_folder=self.persistent_folder,
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
        Retrieves execution logs for all layers.
        """
        logs = self.log_connector.get_all_layer_statuses()
        if logs:
            print("Execution Logs:")
            for log in logs:
                layer_name, status, last_execution, error_message = log
                print(
                    f"Layer: {layer_name}, Status: {status}, Last Execution: {last_execution}, Error: {error_message}")
        else:
            print("No execution logs found.")
        return logs

    def download_last_datasources(self, destination_dir: str = r"data\downloads"):
        """
        Downloads the last data sources from the persistent folder to the specified destination.
        """
        pass
