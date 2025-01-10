from datetime import datetime

import pandas as pd
from sklearn.impute import KNNImputer

from models.layers.storage.trusted import Trusted


class MVCPersonTrusted(Trusted):
    def _get_trusted_table_name(self) -> str:
        return "mvc_person"

    def _list_tables(self) -> list[str]:
        return [
            t
            for t in super()._list_tables()
            if t.startswith("motorvehiclecollisionsperson")
        ]

    def _clean_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates(subset="unique_id").reset_index(drop=True)
        return df

    def _correct_misspellings(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.replace(["Does Not Apply", "Unknown", "None", "Unspecified"], pd.NA)
        return df

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        def one_hot_encode_and_format(df, column_name, prefix):
            # One-hot encoding with formatting in one step
            encoded_df = pd.get_dummies(df[column_name], prefix=prefix)
            return encoded_df

        combined_factors = pd.concat(
            [df["contributing_factor_1"], df["contributing_factor_2"]]
        )

        one_hot_encoded_factors = (
            one_hot_encode_and_format(
                pd.DataFrame(combined_factors), column_name=0, prefix="factor"
            )
            .groupby(level=0)
            .sum()
        )

        df = df.drop(["contributing_factor_1", "contributing_factor_2"], axis=1)
        df = pd.concat([df, one_hot_encoded_factors], axis=1)

        one_hot_encoded_person_type = one_hot_encode_and_format(
            df, "person_type", "person_type"
        )
        df = pd.concat(
            [df.drop("person_type", axis=1), one_hot_encoded_person_type], axis=1
        )

        df["person_injured"] = df["person_injury"].notna().astype(int)
        df = df.drop("person_injury", axis=1)

        df["person_age"] = (
            pd.to_numeric(df["person_age"], errors="coerce")
            .fillna(pd.NA)
            .astype("Int64")
        )
        df = self._transform_column_names_to_snake_case(df)
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        exclude_columns = ["unique_id", "collision_id", "person_id", "vehicle_id"]
        impute_columns = [col for col in df.columns if col not in exclude_columns]

        df_impute = df[impute_columns].copy()
        df_impute = pd.get_dummies(df_impute, columns=["person_sex"], drop_first=True)
        imputer = KNNImputer(n_neighbors=5)

        df_imputed = imputer.fit_transform(df_impute)
        df_imputed = pd.DataFrame(df_imputed, columns=df_impute.columns, index=df.index)

        df["person_age"] = (
            pd.to_numeric(df_imputed["person_age"], errors="coerce")
            .round()
            .astype("Int64")
        )
        return df

    def _drop_insignificant_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        important_columns = [
            "unique_id",
            "collision_id",
            "person_id",
            "person_type",
            "person_injury",
            "vehicle_id",
            "person_age",
            "person_sex",
            "contributing_factor_1",
            "contributing_factor_2",
        ]
        return df[important_columns]
