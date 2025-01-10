from src.helpers.db_connector import (
    DBConnector,
)
from models.layers.layer import Layer
from models.modeling.model_factory import ModelFactory
from abc import abstractmethod
import os


class ModelTrainingLayer(Layer):
    def __init__(
        self,
        feature_db_connector: DBConnector,
        model_storing_path: str,
        model_factory: ModelFactory
    ):
        self.feature_db_connector = feature_db_connector
        self.model_storing_path = model_storing_path
        self.model_factory = model_factory
        self.model = self.model_factory.get_instance()
        self.model.set_feature_db_connector(feature_db_connector)

    def execute(self):
        self.model.create()
        self.model.fit()
        self.model.save(os.path.join(self.model_storing_path, self.model_factory.get_model_filename()))