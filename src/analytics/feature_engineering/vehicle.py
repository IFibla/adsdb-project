import numpy as np
import pandas as pd
from sklearn.impute import IterativeImputer

from models.layers.analytics.feature_engineering import FeatureEngineering
from src.analytics.models.car_make import CarMakeEmbedding
from src.helpers import DBConnector


class AccidentFeatureEngineering(FeatureEngineering):
    """
    A feature engineering process for brand-related data.
    This class extends FeatureEngineering to calculate vehicle age,
    normalize overall ratings, generate vehicle make embeddings, and
    prepare the data for machine learning models.
    """

    def _get_analytical_sandbox_table_name(self) -> str:
        return "safety_rating_by_accidents"

    def _get_feature_engineering_table_name(self) -> str:
        return "safety_rating_by_accidents"

    def _transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the DataFrame by adding vehicle age, normalizing overall ratings,
        generating vehicle make embeddings, and selecting relevant features.

        Args:
            df (pd.DataFrame): The DataFrame to be transformed.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """

        df['vehicle_age'] = 2024 - df['vehicle_year']

        df.drop(columns=['vehicle_year'], inplace=True)
        df.drop(columns=['person_id'], inplace=True)

        df['person_age'].hist()
        df['person_age'] = df['person_age'].replace(0, np.nan)

        df['person_sex'].value_counts().plot(kind='bar')
        df['person_sex'].isna().sum()

        df["vehicle_make_embedding"] = df["vehicle_make"].apply(lambda x: self.cme.execute(x)[0])
        make_df = pd.DataFrame(
            df["vehicle_make_embedding"].tolist(),
            columns=[f"make_{i}" for i in range(len(df["vehicle_make_embedding"][0]))],
        )
        df = pd.concat([df.drop(columns=["vehicle_make_embedding"]), make_df], axis=1)
        df.drop(columns=['vehicle_make'], inplace=True)

        df['overall_rating'].hist()
        df['overall_rating'] = df['overall_rating'].clip(lower=0, upper=5)
        df['overall_rating'] = np.round(df['overall_rating'] * 2) / 2

        df_encoded = df.copy()
        df_encoded['person_sex'] = df_encoded['person_sex'].astype('category').cat.codes

        mice_imputer = IterativeImputer(max_iter=10, random_state=42)
        columns_to_impute = ['person_age', 'person_sex', 'overall_rating']

        df_imputed_array = mice_imputer.fit_transform(df_encoded[columns_to_impute])
        df_imputed = pd.DataFrame(df_imputed_array, columns=columns_to_impute)

        sex_mapping = dict(enumerate(df['person_sex'].astype('category').cat.categories))
        df_imputed['person_sex'] = df_imputed['person_sex'].round().astype(int).map(sex_mapping)

        df.update(df_imputed)

        sex = pd.get_dummies(df['person_sex'])
        df = pd.concat([sex, df], axis=1)
        df.drop(columns=['person_sex'], inplace=True)

        df['overall_rating'] = df['overall_rating'].clip(lower=0, upper=5)
        df['overall_rating'] = (df['overall_rating'] * 2).round() / 2

        df['person_age'] = df['person_age'].astype(int)

        return df
