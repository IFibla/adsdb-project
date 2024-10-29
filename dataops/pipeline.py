import src
from src.helpers import DBConnector
from src.helpers import LogDBConnector  # Import the new LogDBConnector
from src.landing.landing import Landing


class Pipeline:
    def __init__(
        self,
        temporal_folder: str = r"data\landing\temporal",
        persistent_folder: str = r"data\landing\persistent",
    ):
        self.temporal_folder = temporal_folder
        self.persistent_folder = persistent_folder

        self._load_connectors()

        self.control_connector = LogDBConnector(db_path="execution_log.db")
        self.control_connector.create_execution_log_table()

        self.stages = {
            "landing": self.landing_phase,
            "trusted": self.trusted_phase,
            "formatted": self.formatted_phase,
            "exploitation": self.exploitation_phase,
        }

    def _load_connectors(self) -> None:
        self.connectors = {
            "landing_connector": DBConnector(),
            "trusted_connector": DBConnector(),
            "formatted_connector": DBConnector(),
            "exploitation_connector": DBConnector(),
        }

    def _execute_phase(self, phase_name: str, module, connector_name: str):
        print(f"Executing {phase_name} phase...")

        loaded_classes = [getattr(module, cls_name) for cls_name in module.__all__]

        for cls in loaded_classes:
            layer_name = cls.__name__
            try:
                self.control_connector.update_execution_status(
                    layer_name, "executing"
                )
                instance = cls(
                    self.persistent_folder, self.connectors.get(connector_name)
                )
                print(f"Executing {layer_name} in {phase_name} phase")
                instance.execute()
                self.control_connector.update_execution_status(layer_name, "done")
            except Exception as e:
                self.control_connector.update_execution_status(
                    layer_name, "failed", str(e)
                )
                print(f"Error executing {layer_name}: {e}")

        print(f"{phase_name.capitalize()} phase completed.")

    def landing_phase(self):
        self._execute_phase("landing", src.landing, "landing_connector")

    def formatted_phase(self):
        self._execute_phase("formatted", src.formatted, "formatted_connector")

    def trusted_phase(self):
        self._execute_phase("trusted", src.trusted, "trusted_connector")

    def exploitation_phase(self):
        self._execute_phase("exploitation", src.exploitation, "exploitation_connector")

    def execute_stage(self, stage_name):
        """Executes a specific phase if it exists in the defined layers"""
        if stage_name in self.stages:
            self.stages[stage_name]()
        else:
            print(f"Stage '{stage_name}' not found in pipeline.")

    def execute_all_stages(self):
        """Executes all phases of the pipeline in order"""
        for stage in self.stages:
            self.stages[stage]()


if __name__ == "__main__":
    print("Testing pipeline")
    pipeline = Pipeline()
    pipeline.execute_stage("trusted")
