from abc import ABC, abstractmethod

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    f1_score,
    confusion_matrix,
    recall_score,
)

from src.helpers import DBConnector


class Model(ABC):
    def __init__(self):
        self.feature_db_connector = None
        self.model = None

    def set_feature_db_connector(self, feature_db_connector: DBConnector):
        self.feature_db_connector = feature_db_connector

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self, x: pd.DataFrame):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def get_metrics(self, y_test, y_pred):
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @abstractmethod
    def load(self, path: str):
        pass

    @abstractmethod
    def get_target_column_name(self):
        pass

    @abstractmethod
    def get_training_table_name(self):
        pass

    @abstractmethod
    def get_testing_table_name(self):
        pass
