import os

import pandas as pd

from models.storage.layers.formatted import Formatted


class JSONFormatted(Formatted):
    def _list_files(self) -> list[str]:
        return [
            os.path.join(self.persistent_folder, f)
            for f in os.listdir(self.persistent_folder)
            if f.endswith('.json')
        ]

    def _read_file(self, path: str) -> pd.DataFrame:
        try:
            return pd.read_json(path)
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return pd.DataFrame()
