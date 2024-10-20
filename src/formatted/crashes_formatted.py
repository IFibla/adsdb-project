from models.storage.layers.formatted import Formatted
from pandas import DataFrame

class CrashesFormatted(Formatted):
    def format_data(self, data: DataFrame) -> DataFrame:
        dataset_version = data['metadata_date'].iloc[0]
        self.m_db_connector.insert_data(f'crashes_{dataset_version}', data)