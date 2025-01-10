from abc import ABC, abstractmethod

import joblib
import pandas as pd
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

    @abstractmethod
    def create(self):
        pass

    def fit(self):
        train_df = self.feature_db_connector.get_table_as_dataframe(self.get_training_table_name())
        X_train = train_df.drop(columns=[self.get_target_column_name()])
        y_train = train_df[self.get_target_column_name()]
        self.model.fit(X_train, y_train)

    def predict(self, x: pd.DataFrame):
        return self.model.predict(x)

    def validate(self):
        test_df = self.feature_db_connector.get_table_as_dataframe(self.get_testing_table_name())
        x_test = test_df.drop(columns=[self.get_target_column_name()])
        return test_df[self.get_target_column_name()], self.predict(x_test)

    @abstractmethod
    def get_metrics(self, y_test, y_pred) -> dict:
        pass

    def save(self, path: str):
        if self.model is None:
            raise ValueError(
                "Model is not created. Please call create() before saving."
            )
        joblib.dump(self.model, path)

    def load(self, path: str):
        self.model = joblib.load(path)
