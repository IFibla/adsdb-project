import json
import os

import pandas as pd

from models.storage.layers.formatted import Formatted


class JSONFormatted(Formatted):
    def _list_files(self) -> list[str]:
        return [
            os.path.splitext(x)[0]
            for x in super()._list_files()
            if x.endswith(".json")
        ]

    def _read_file(self, path: str) -> pd.DataFrame:
        try:
            with open(f"{self.persistent_folder}{os.path.sep}{path}.json", "r") as f:
                data = json.load(f)

            api_response_list = data.get("apiResponse", [])
            df_list = []

            for response in api_response_list:
                results = response.get("Results", [])
                if results:
                    df = pd.json_normalize(results)
                    df_list.append(df)

            if df_list:
                df = pd.concat(df_list, ignore_index=True)
            else:
                df = pd.DataFrame()

            return df

        except Exception as e:
            print(f"Error reading file {path}: {e}")
            return pd.DataFrame()
