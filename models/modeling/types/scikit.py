from abc import ABC, abstractmethod

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from models.modeling.model import Model
from src.helpers import DBConnector


class SciKitModel(Model, ABC):
    def __init__(self, feature_db_connector: DBConnector):
        super().__init__(feature_db_connector)

    @abstractmethod
    def create(self):
        pass

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    @abstractmethod
    def get_metrics(self, y_test, y_pred)-> dict:
        pass

    def save(self, path: str):
        if self.model is None:
            raise ValueError(
                "Model is not created. Please call create() before saving."
            )
        joblib.dump(self.model, path)

    def load(self, path: str):
        self.model = joblib.load(path)
