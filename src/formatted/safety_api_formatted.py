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
        return pd.DataFrame(data)
