from datetime import datetime
from typing import Optional, List

from src.helpers import DBConnector


class LogDBConnector(DBConnector):
    """
    Specialized connector for handling execution log operations.
    Inherits from DBConnector to utilize the existing database connection.
    """

    def create_execution_log_table(self):
        """
        Creates the execution_log table if it does not exist.
        """
        query = """
        CREATE TABLE IF NOT EXISTS execution_log (
            layer_name VARCHAR PRIMARY KEY,
            execution_status VARCHAR,
            last_execution TIMESTAMP,
            error_message VARCHAR
        )
        """
        self.execute_query(query)

    def update_execution_status(
        self, layer_name: str, status: str, error_message: Optional[str] = None
    ):
        """
        Updates the execution status of a layer.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message_value = f"'{error_message}'" if error_message else "NULL"

        query = f"""
        INSERT INTO execution_log (layer_name, execution_status, last_execution, error_message)
        VALUES ('{layer_name}', '{status}', '{timestamp}', {error_message_value})
        ON CONFLICT (layer_name) DO UPDATE SET
            execution_status = EXCLUDED.execution_status,
            last_execution = EXCLUDED.last_execution,
            error_message = EXCLUDED.error_message
        """
        self.execute_query(query)

    def get_layer_status(self, layer_name: str) -> Optional[tuple]:
        """
        Retrieves the execution status of a specific layer.
        """
        query = f"SELECT * FROM execution_log WHERE layer_name = '{layer_name}'"
        result = self.execute_query(query)
        if result:
            return result[0]
        else:
            return None

    def get_all_layer_statuses(self) -> List[tuple]:
        """
        Retrieves the execution status of all layers.
        """
        query = "SELECT * FROM execution_log"
        return self.execute_query(query)
