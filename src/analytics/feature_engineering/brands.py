from models.layers.analytics.feature_engineering import FeatureEngineering
from datetime import date
import pandas as pd


class BrandsFeatureEngineering(FeatureEngineering):
    """
    A feature engineering process for brand-related data.
    This class extends FeatureEngineering to calculate vehicle age,
    normalize overall ratings, generate vehicle make embeddings, and
    prepare the data for machine learning models.
    """

    def _get_analytical_sandbox_table_name(self) -> str:
        return "mvc_safety_rating_by_brand"

    def _get_feature_engineering_table_name(self) -> str:
        return "mvc_safety_rating_by_brand"

    def _transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the DataFrame by adding vehicle age, normalizing overall ratings,
        generating vehicle make embeddings, and selecting relevant features.

        Args:
            df (pd.DataFrame): The DataFrame to be transformed.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """
        df["vehicle_age"] = date.today().year - df["vehicle_year"]
        df["norm_overall_rating"] = df["overall_rating"] / 5

        # Generate vehicle make embeddings
        df["vehicle_make_embedding"] = df["vehicle_make"].apply(
            lambda x: self.cme.execute(x)[0]
        )
        make_df = pd.DataFrame(
            df["vehicle_make_embedding"].tolist(),
            columns=[f"make_{i}" for i in range(len(df["vehicle_make_embedding"][0]))],
        )
        df = pd.concat([df.drop(columns=["vehicle_make_embedding"]), make_df], axis=1)

        # Drop rows with missing values
        df.dropna(inplace=True)

        # Select relevant features
        df = df[
            [f"make_{i}" for i in range(10)] + ["vehicle_age", "norm_overall_rating"]
        ]  # Include normalized rating

        return df
