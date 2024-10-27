from models.storage.layers.formatted import Formatted
import pandas as pd
import re
import os


class CSVFormatted(Formatted):
    def _list_files(self) -> list[str]:
        return list(filter(lambda x: x.endswith(".csv"), super()._list_files()))

    def _read_file(self, path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(f"{self.persistent_folder}{os.path.sep}{path}")
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return pd.DataFrame()

    def compute_table_name(self, filename: str) -> str:
        return "_".join(
            map(
                lambda x: re.sub(
                    pattern="[^a-zA-Z\d\s:]",
                    repl="",
                    string=x.lower(),
                ),
                filename[:-4].split("/")[-3:],
            )
        )
