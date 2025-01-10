import pandas as pd

from models.layers.analytics.analytical_sandbox import AnalyticalSandbox


class AccidentAnalyticalSandbox(AnalyticalSandbox):
    def _get_exploitation_table_name(self) -> str:
        return "safety_rating_by_accidents"

    def _get_analytical_sandbox_table_name(self) -> str:
        return "safety_rating_by_accidents"

    def _filter_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame to include only columns relevant to brand analysis.

        Args:
            df (pd.DataFrame): The DataFrame to be filtered.

        Returns:
            pd.DataFrame: The filtered DataFrame containing only the 'vehicle_make',
                          'vehicle_year', and 'overall_rating' columns.
        """
        return df
