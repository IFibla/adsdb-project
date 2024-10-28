import src
from models.storage.layers.landing import Landing
from src.helpers import DBConnector


class Pipeline:
    def __init__(
        self,
        temporal_folder: str = r"data\landing\temporal",
        persistent_folder: str = r"data\landing\persistent",
    ):
        self.temporal_folder = temporal_folder
        self.persistent_folder = persistent_folder

        self._load_connectors()

        self.control_connector = DBConnector(db_path="execution_log.db")
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
            "formatted_connector": DBConnector(),
            "trusted_connector": DBConnector(),
            "exploitation_connector": DBConnector(),
        }

    def _execute_phase(self, phase_name: str, module, connector_name: str):
        print(f"Executing {phase_name} phase...")

        loaded_classes = [getattr(module, cls_name) for cls_name in module.__all__]

        for cls in loaded_classes:
            layer_name = cls.__name__
            try:
                self.control_connector.update_execution_status(
                    layer_name, "en ejecución"
                )

                instance = cls(
                    self.persistent_folder, self.connectors.get(connector_name)
                )
                print(f"Executing {layer_name} in {phase_name} phase")
                instance.execute()

                self.control_connector.update_execution_status(layer_name, "completada")
            except Exception as e:
                self.control_connector.update_execution_status(
                    layer_name, "fallida", str(e)
                )
                print(f"Error executing {layer_name}: {e}")

        print(f"{phase_name.capitalize()} phase completed.")

    def landing_phase(self):
        print("Executing landing phase...")
        landing = Landing(
            temporal_folder=self.temporal_folder,
            persistent_folder=self.persistent_folder,
        )
        landing.execute()
        print("Landing phase completed.")

    def trusted_phase(self):
        self._execute_phase("trusted", src.trusted, "trusted_connector")

    def formatted_phase(self):
        self._execute_phase("formatted", src.formatted, "formatted_connector")

    def exploitation_phase(self):
        self._execute_phase("exploitation", src.exploitation, "exploitation_connector")

    def execute_stage(self, stage_name):
        """Ejecuta una fase específica si existe en las capas definidas"""
        if stage_name in self.stages:
            self.stages[stage_name]()
        else:
            print(f"Stage '{stage_name}' not found in pipeline.")

    def execute_all_stages(self):
        """Ejecuta todas las fases del pipeline en orden"""
        for stage in self.stages:
            self.stages[stage]()


if __name__ == "__main__":
    print("Testing pipeline")
    pipeline = Pipeline()
    pipeline.execute_stage("trusted")
