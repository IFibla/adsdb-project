import pandas as pd

from models.storage.layers.formatted import Formatted


class SafetyApiFormatted(Formatted):
    """
    Concrete class representing a formatted layer specifically for Safety API data.

    The SafetyApiFormatted class takes raw data from a SafetyApiLanding layer and transforms it into
    a standardized pandas DataFrame format.

    Methods:
        format_data(data: Any) -> DataFrame:
            Transforms the raw data from the Safety API into a standardized DataFrame.
    """

    def format_data(self, data: dict) -> pd.DataFrame:
        df = pd.DataFrame([result.dict() for item in data for result in item.results])
        self.m_db_connector.insert_data("safety_api_results", df)
        return df
