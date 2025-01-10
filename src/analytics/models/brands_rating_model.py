from sklearn.ensemble import RandomForestClassifier
from models.modeling.types.scikit import SciKitModel
from sklearn.metrics import f1_score, confusion_matrix


class BrandsRatingModel(SciKitModel):
    def get_target_column_name(self):
        return "overall_rating"

    def get_training_table_name(self):
        return "mvc_safety_rating_by_brand_train"

    def get_testing_table_name(self):
        return "mvc_safety_rating_by_brand_test"

    def create(self):
        self.model = RandomForestClassifier(max_depth=10, n_estimators=200)

    def get_metrics(self, y_test, y_pred) -> dict:
        return {
            "macro": f1_score(y_test, y_pred, average="macro"),
            "micro": f1_score(y_test, y_pred, average="micro"),
            "weighted": f1_score(y_test, y_pred, average="weighted"),
            "raw": f1_score(y_test, y_pred, average=None),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
        }


