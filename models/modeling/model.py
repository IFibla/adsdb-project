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
    def __init__(self, feature_db_connector: DBConnector):
        self.feature_db_connector = feature_db_connector
        self.model = None

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def fit(self, training_table, target_column):
        pass

    @abstractmethod
    def predict(self, testing_table, target_column):
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

    def train(self):
        if self.model is None:
            raise ValueError("Model not created yet. Call create() first.")
        if self.train_df is None:
            raise ValueError(
                "Training data not provided. Set train_df before calling train()"
            )

        target_column_name = self.get_target_column_name()

        if target_column_name not in self.train_df.columns:
            raise ValueError(
                f"Target column '{target_column_name}' not found in the training data."
            )

        X_train = self.train_df.drop(target_column_name, axis=1)
        y_train = self.train_df[target_column_name]

        self.fit(X_train, y_train)

    def validate(self):
        if self.model is None:
            raise ValueError("Model not created yet. Call create() first.")
        if self.test_df is None:
            raise ValueError(
                "Test data not provided. Set test_df before calling validate()"
            )

        target_column_name = self.get_target_column_name()

        if target_column_name not in self.test_df.columns:
            raise ValueError(
                f"Target column '{target_column_name}' not found in the test data."
            )

        X_test = self.test_df.drop(target_column_name, axis=1)
        y_test = self.test_df[target_column_name]

        y_pred = self.predict(X_test)

        metrics = self.get_metrics(y_test, y_pred)

        return metrics

    @abstractmethod
    def get_target_column_name(self):
        pass

    @abstractmethod
    def get_training_table_name(self):
        pass

    @abstractmethod
    def get_testing_table_name(self):
        pass
