import re

import pandas as pd

from models.storage.layers.trusted import Trusted


class NHTSASafetyRatingTrusted(Trusted):
    def _get_trusted_table_name(self) -> str:
        return "nhtsa_safety_rating"

    def _transform_column_names_to_snake_case(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [
            re.sub(r"(?<!^)(?=[A-Z])", "_", col.replace("NHTSA", "nhtsa"))
            .replace("-", "_")
            .lower()
            for col in df.columns
        ]
        return df

    def _list_tables(self) -> list[str]:
        return [
            table
            for table in super()._list_tables()
            if table.startswith("nhtsa_safety_rating")
        ]

    def _clean_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates(subset="vehicle_id").reset_index(drop=True)
        return df

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.set_index("vehicle_id", drop=True)
        return df

    def _remove_additional_ratings(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[["make", "model", "model_year", "overall_rating"]]

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.replace("Not Rated", pd.NA).convert_dtypes()

        df["overall_rating"] = pd.to_numeric(
            df["overall_rating"], errors="coerce"
        ).astype("Float64")

        for index, row in df[df["overall_rating"].isna()].iterrows():
            rating_cols = [
                col
                for col in df.columns
                if "rating" in col.lower() and col != "overall_rating"
            ]
            valid_ratings = row[rating_cols].dropna().astype(float)

            if not valid_ratings.empty:
                df.at[index, "overall_rating"] = valid_ratings.mean()

        df["overall_rating"] = df.groupby(["make", "model"])[
            "overall_rating"
        ].transform(lambda x: x.fillna(x.mean()))

        df["overall_rating"] = df.groupby("make")["overall_rating"].transform(
            lambda x: x.fillna(x.mean())
        )

        return self._remove_additional_ratings(df)

    def _drop_insignificant_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        significant_columns = [
            "vehicle_id",
            "make",
            "model",
            "model_year",
        ]

        rating_columns = [col for col in df.columns if "rating" in col.lower()]

        columns_to_keep = significant_columns + rating_columns
        return df[columns_to_keep]
