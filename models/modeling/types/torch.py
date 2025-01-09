import abc
from abc import abstractmethod

import torch
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from models.modeling.model import Model
from src.helpers import DBConnector


class TorchModel(Model, abc.ABC):
    def __init__(self, feature_db_connector: DBConnector):
        super().__init__(feature_db_connector)

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def fit(self, X_train, y_train):
        pass

    def predict(self, X_test):
        self.model.eval()
        with torch.no_grad():
            X_test_tensor = torch.tensor(X_test).float()
            outputs = self.model(X_test_tensor)
            _, predicted = torch.max(outputs, 1)
        return predicted.numpy()

    @abstractmethod
    def get_metrics(self, y_test, y_pred) -> dict:
        pass

    def save(self, path: str):
        if self.model is None:
            raise ValueError(
                "Model is not created. Please call create() before saving."
            )
        torch.save(self.model.state_dict(), path)

    def load(self, path: str):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()
