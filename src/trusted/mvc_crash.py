from models.storage.layers.trusted import Trusted
from sklearn.impute import KNNImputer
import pandas as pd
import numpy as np


class MVCCrash(Trusted):
    def _get_trusted_table_name(self) -> str:
        return "mvc_crash"

    def _list_tables(self) -> list[str]:
        return list(filter(lambda x: "motorvehiclecollisionscrashes" in x, super()._list_tables()))

    def _drop_insignificant_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(
            [
                "borough",
                "zip_code",
                "latitude",
                "longitude",
                "location",
                "on_street_name",
                "cross_street_name",
                "off_street_name",
                "vehicle_type_code_1",
                "vehicle_type_code_2",
                "vehicle_type_code_3",
                "vehicle_type_code_4",
                "vehicle_type_code_5",
            ],
            axis=1,
        )

    def _clean_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates("collision_id")
        return df.reset_index()

    def _correct_misspellings(self, df: pd.DataFrame) -> pd.DataFrame:
        misspelling_mapping = {
            "1": np.nan,
            "80": np.nan,
            "Cell Phone (hand-Held)": "Cell Phone (hand-held)",
            "Drugs (Illegal)": "Drugs (illegal)",
            "Illnes": "Illness",
            "Reaction to Other Uninvolved Vehicle": "Reaction to Uninvolved Vehicle",
            "Unspecified": np.nan,
        }
        for idx in range(1, 6):
            for correction in misspelling_mapping:
                df[f"contributing_factor_vehicle_{idx}"] = df[
                    f"contributing_factor_vehicle_{idx}"
                ].replace(
                    to_replace=correction["pattern"],
                    value=correction["replacement"],
                )
        return df

    def _format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        def transform_contributing_factor_to_onehot(df: pd.DataFrame) -> pd.DataFrame:
            df["contributing_factor_vehicle"] = df[
                [f"contributing_factor_vehicle_{i}" for i in range(1, 6)]
            ].apply(lambda row: row.dropna().tolist(), axis=1)
            df = df.drop(
                [f"contributing_factor_vehicle_{i}" for i in range(1, 6)],
                axis=1,
            )
            df = pd.concat(
                [
                    df,
                    pd.get_dummies(df["contributing_factor_vehicle"].explode())
                    .groupby(level=0)
                    .sum(),
                ],
                axis=1,
            )
            return df.drop("contributing_factor_vehicle", axis=1)

        def transform_datetime_to_utc(df: pd.DataFrame) -> pd.DataFrame:
            df["crash_datetime"] = pd.to_datetime(
                df["crash_date"] + " " + df["crash_time"]
            )
            return df.drop(["crash_date", "crash_time"], axis=1)

        df = transform_contributing_factor_to_onehot(df)
        df = self._transform_column_names_to_snake_case(df)
        df = transform_datetime_to_utc(df)
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(["collision_id", "crash_datetime"])
        impute_columns = [
            col for col in df.columns if col not in ["collision_id", "crash_datetime"]
        ]
        imputer = KNNImputer(n_neighbors=5)
        df[impute_columns] = imputer.fit_transform(df[impute_columns])
        return df
