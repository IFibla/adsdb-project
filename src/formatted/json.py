import os

import pandas as pd

from models.storage.layers.formatted import Formatted


class JSONFormatted(Formatted):
    def _list_files(self) -> list[str]:
        return list(filter(lambda x: x.endswith(".json"), super()._list_files()))

    def _read_file(self, path: str) -> pd.DataFrame:
        try:
            return pd.read_json(f"{self.persistent_folder}{os.path.sep}{path}")
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return pd.DataFrame()
