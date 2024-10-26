from models.storage.layers.formatted import Formatted
import pandas as pd


class CSVFormatted(Formatted):
    def _list_files(self) -> list[str]:
        return list(filter(lambda x: x.endswith(".csv", super()._list_files())))

    def _read_file(self, path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(path)
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return pd.DataFrame()