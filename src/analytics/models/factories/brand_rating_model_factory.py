from models.modeling.model_factory import ModelFactory
from src.analytics.models.brands_rating_model import BrandsRatingModel


class BrandRatingModelFactory(ModelFactory):
    def get_instance(self):
        return BrandsRatingModel()

    def get_model_filename(self):
        return "brand_rating_model.pkl"
