from models.modeling.model_factory import ModelFactory
from src.analytics.models.accident_rating_model import AccidentRatingModel


class AccidentRatingModelFactory(ModelFactory):

    def get_instance(self):
        return AccidentRatingModel()

    def get_model_filename(self):
        return "accident_rating_model.pkl"
