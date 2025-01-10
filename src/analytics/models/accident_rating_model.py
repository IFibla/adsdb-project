from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from models.modeling.types.scikit import SciKitModel


class AccidentRatingModel(SciKitModel):
    def get_training_table_name(self):
        return "safety_rating_by_accidents_train"

    def get_testing_table_name(self):
        return "safety_rating_by_accidents_test"

    def get_target_column_name(self):
        return "overall_rating"

    def create(self):
        self.model = RandomForestRegressor(max_depth=10, n_estimators=200)

    def get_metrics(self, y_test, y_pred) -> dict:
        return {
            "mean_absolute_error": mean_absolute_error(y_test, y_pred),
            "mean_squared_error": mean_squared_error(y_test, y_pred),
            "root_mean_squared_error": mean_squared_error(y_test, y_pred, squared=False),
            "r2_score": r2_score(y_test, y_pred),
        }
