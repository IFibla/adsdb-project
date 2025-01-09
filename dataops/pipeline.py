import os
import src
from src.helpers import DBConnector
from src.helpers import LogDBConnector  # Import the new LogDBConnector


class Pipeline:
    def __init__(
        self,
        temporal_folder: str = r"data\landing\temporal",
        persistent_folder: str = r"data\landing\persistent",
        connector_folder: str = r"data",
    ):
        self.temporal_folder = temporal_folder
        self.persistent_folder = persistent_folder
        self.connector_folder = connector_folder

        self._load_connectors()

        self.control_connector = LogDBConnector(db_path="execution_log.db")
        self.control_connector.create_execution_log_table()

        self.stages = {
            "landing": self.landing_phase,
            "formatted": self.formatted_phase,
            "trusted": self.trusted_phase,
            "exploitation": self.exploitation_phase,
        }

        self.phase_constructor_args = {
            "landing": self._landing_constructor_args,
            "formatted": self._formatted_constructor_args,
            "trusted": self._trusted_constructor_args,
            "exploitation": self._exploitation_constructor_args,
        }

    def _load_connectors(self) -> None:
        self.connectors = {
            "formatted_connector": DBConnector(
                db_path=os.path.join(self.connector_folder, "formatted.duckdb")
            ),
            "trusted_connector": DBConnector(
                db_path=os.path.join(self.connector_folder, "trusted.duckdb")
            ),
            "exploitation_connector": DBConnector(
                db_path=os.path.join(self.connector_folder, "exploitation.duckdb")
            ),
        }

    def _landing_constructor_args(self, cls):
        return cls(self.temporal_folder, self.persistent_folder)

    def _formatted_constructor_args(self, cls):
        return cls(self.persistent_folder, self.connectors.get("formatted_connector"))

    def _trusted_constructor_args(self, cls):
        return cls(
            self.connectors.get("formatted_connector"),
            self.connectors.get("trusted_connector"),
        )

    def _exploitation_constructor_args(self, cls):
        return cls(
            self.connectors.get("trusted_connector"),
            self.connectors.get("exploitation_connector"),
        )

    def _execute_phase(self, phase_name: str, module, connector_name: str):
        print(f"Executing {phase_name} phase...")

        loaded_classes = [getattr(module, cls_name) for cls_name in module.__all__]

        for cls in loaded_classes:
            layer_name = cls.__name__
            try:
                self.control_connector.update_execution_status(layer_name, "executing")
                constructor_func = self.phase_constructor_args.get(phase_name)
                if not constructor_func:
                    raise ValueError(
                        f"No constructor function defined for phase '{phase_name}'"
                    )

                instance = constructor_func(cls)

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
        """Executes a specific phase if it exists in the defined storage"""
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
