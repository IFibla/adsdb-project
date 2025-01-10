import os
import src
from models.layers.analytics.model_predictor import ModelPredictorLayer
from models.layers.analytics.model_training import ModelTrainingLayer
from models.layers.analytics.model_validator import ModelValidatorLayer
from src.analytics.feature_engineering import BrandsFeatureEngineering
from src.analytics.models.factories.accident_rating_model_factory import AccidentRatingModelFactory
from src.analytics.models.factories.brand_rating_model_factory import BrandRatingModelFactory
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
            "analytical_sandbox": self.analytical_sandbox_phase,
            "feature_engineering": self.feature_engineering_phase,
        }

        self.phase_constructor_args = {
            "landing": self._landing_constructor_args,
            "formatted": self._formatted_constructor_args,
            "trusted": self._trusted_constructor_args,
            "exploitation": self._exploitation_constructor_args,
            "analytical_sandbox": self._analytical_sandbox_constructor_args,
            "feature_engineering": self._feature_engineering_constructor_args,
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
            "analytical_sandbox_connector": DBConnector(
                db_path=os.path.join(self.connector_folder, "analytical_sandbox.duckdb")
            ),
            "feature_engineering_connector": DBConnector(
                db_path=os.path.join(self.connector_folder, "feature_engineering.duckdb")
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

    def _analytical_sandbox_constructor_args(self, cls):
        return cls(
            self.connectors.get("exploitation_connector"),
            self.connectors.get("analytical_sandbox_connector"),
        )

    def _feature_engineering_constructor_args(self, cls):
        return cls(
            self.connectors.get("analytical_sandbox_connector"),
            self.connectors.get("feature_engineering_connector"),
        )

    def _execute_phase(self, phase_name: str, module):
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
        self._execute_phase("landing", src.landing)

    def formatted_phase(self):
        self._execute_phase("formatted", src.formatted)

    def trusted_phase(self):
        self._execute_phase("trusted", src.trusted)

    def exploitation_phase(self):
        self._execute_phase("exploitation", src.exploitation)

    def analytical_sandbox_phase(self):
        self._execute_phase("analytical_sandbox", src.analytical_sandbox)

    def feature_engineering_phase(self):
        self._execute_phase("feature_engineering", src.feature_engineering)

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

        self._train_models()
        return self._validate_models()

    def _train_models(self):
        # Due to the limited remaining time, we won't import dynamically the classes
        ModelTrainingLayer(self.connectors.get("feature_engineering_connector"), r"./data/models", AccidentRatingModelFactory()).execute()
        ModelTrainingLayer(self.connectors.get("feature_engineering_connector"), r"./data/models", BrandRatingModelFactory()).execute()

    def _validate_models(self):
        # Due to the limited remaining time, we won't import dynamically the classes
        metrics_accident = ModelValidatorLayer(self.connectors.get("feature_engineering_connector"), r"./data/models",
                           AccidentRatingModelFactory()).execute()
        metrics_brand = ModelValidatorLayer(self.connectors.get("feature_engineering_connector"), r"./data/models",
                           BrandRatingModelFactory()).execute()
        return {"accident": metrics_accident, "brand": metrics_brand}


if __name__ == "__main__":
    print("Testing pipeline")
    pipeline = Pipeline()
    pipeline.execute_stage("trusted")
