from src.helpers.db_connector import (
    DBConnector,
)
from models.modeling.model_factory import ModelFactory
from models.layers.layer import Layer
from abc import abstractmethod
import pandas as pd
import os


class ModelPredictorLayer(Layer):
    def __init__(
        self,
        model_storing_path: str,
        predictor_dataframe: pd.DataFrame,
        model_factory: ModelFactory
    ):
        self.predictor_dataframe = predictor_dataframe
        self.model_storing_path = model_storing_path
        self.model_factory = model_factory
        self.model = self.model_factory.get_instance()

    def execute(self):
        self.model.load(os.path.join(self.model_storing_path, self.model_factory.get_model_filename()))
        y_pred = self.model.predict(self.predictor_dataframe)
        return y_pred