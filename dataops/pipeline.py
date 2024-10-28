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

    def landing_phase(self):
        print("Executing landing phase...")
        landing = Landing(
            temporal_folder=self.temporal_folder,
            persistent_folder=self.persistent_folder,
        )
        landing.execute()
        print("Landing phase completed.")

    def trusted_phase(self):
        print("Executing trusted phase...")

        loaded_classes = [
            getattr(src.trusted, cls_name) for cls_name in src.trusted.__all__
        ]

        for cls in loaded_classes:
            instance = cls(
                self.persistent_folder, self.connectors.get("trusted_connector")
            )
            print(f"Executing {cls.__name__} in trusted phase")
            instance.execute()

        print("Trusted phase completed.")

    def formatted_phase(self):
        print("Executing formatted phase...")

        loaded_classes = [
            getattr(src.formatted, cls_name) for cls_name in src.formatted.__all__
        ]

        for cls in loaded_classes:
            instance = cls(
                self.persistent_folder, self.connectors.get("formatted_connector")
            )
            instance.execute()

        print("Formatted phase completed.")

    def exploitation_phase(self):
        print("Executing exploitation phase...")

        loaded_classes = [
            getattr(src.exploitation, cls_name) for cls_name in src.exploitation.__all__
        ]

        for cls in loaded_classes:
            instance = cls(
                self.persistent_folder, self.connectors.get("exploitation_connector")
            )
            print(f"Executing {cls.__name__} in exploitation phase")
            instance.execute()

        print("Exploitation phase completed.")

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
