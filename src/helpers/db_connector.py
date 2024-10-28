import duckdb
import pandas as pd


class DBConnector:
    """
    Class to manage connections and operations with a DuckDB database.

    The DBConnector class is designed to interact with specific subtypes of Layer, providing
    methods to execute queries and manage the underlying DuckDB database.
    """

    def __init__(self, db_path: str = ":memory:", read_only: bool = False):
        """
        Initializes the DBConnector instance and connects to the DuckDB database.

        Args:
            db_path (str): Path to the DuckDB database file. Defaults to an in-memory database.
        """
        self.connection = duckdb.connect(database=db_path, read_only=read_only)

    def create_execution_log_table(self):
        """
        Creates the execution_log table if it does not exist.
        """
        query = """
        CREATE TABLE IF NOT EXISTS execution_log (
            layer_name VARCHAR,
            execution_status VARCHAR,
            last_execution TIMESTAMP,
            error_message VARCHAR
        )
        """
        self.execute_query(query)

    def update_execution_status(
        self, layer_name: str, status: str, error_message: str = None
    ):
        """
        Updates the execution status of a layer.
        """
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if error_message:
            error_message = f"'{error_message}'"
        else:
            error_message = "NULL"

        query = f"""
        INSERT INTO execution_log (layer_name, execution_status, last_execution, error_message)
        VALUES ('{layer_name}', '{status}', '{timestamp}', {error_message})
        ON CONFLICT (layer_name) DO UPDATE SET
            execution_status = '{status}',
            last_execution = '{timestamp}',
            error_message = {error_message}
        """
        self.execute_query(query)

    def get_layer_status(self, layer_name: str):
        """
        Retrieves the execution status of a specific layer.
        """
        query = f"SELECT * FROM execution_log WHERE layer_name = '{layer_name}'"
        result = self.execute_query(query)
        if result:
            return result[0]
        else:
            return None

    def get_all_layer_statuses(self):
        """
        Retrieves the execution status of all layers.
        """
        query = "SELECT * FROM execution_log"
        return self.execute_query(query)

    def execute_query(self, query: str) -> list:
        """
        Executes a query against the DuckDB database and returns the result.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            list: Dictionary returned from the executed query
        """
        try:
            self.connection.execute(query)
            return self.connection.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    def insert_data(self, table_name: str, data: pd.DataFrame) -> None:
        """
        Inserts data into a specific table in the DuckDB database.

        Args:
            table_name (str): The name of the table where the data will be inserted.
            data (pd.Dataframe): The data to be inserted. Can be a pandas DataFrame or other compatible format.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        try:
            self.connection.register("data", data)
            self.connection.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM data"
            )
        except Exception as e:
            print(f"Error inserting data: {e}")

    def exists_table(self, table_name: str) -> bool:
        try:
            query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
            result = self.connection.execute(query).fetchone()[0]
            return result > 0
        except Exception as e:
            print(f"Error checking if table exists: {e}")
            return False

    def get_tables(self) -> list[str]:
        try:
            query = f"SELECT table_name FROM information_schema.tables"
            self.connection.execute(query)
            return list(map(lambda x: x[0], self.connection.fetchall()))
        except Exception as e:
            print(f"Error returning all tables: {e}")
            return []

    def get_table_as_dataframe(self, table_name: str) -> pd.DataFrame:
        """
        Retrieves the content of the specified table as a pandas DataFrame.

        Args:
            table_name (str): The name of the table to retrieve.

        Returns:
            pd.DataFrame: The table content as a DataFrame.
        """
        try:
            query = f"SELECT * FROM {table_name}"
            df = self.connection.execute(query).fetchdf()
            return df
        except Exception as e:
            print(f"Error retrieving table '{table_name}': {e}")
            return pd.DataFrame()

    def close_connection(self) -> None:
        """
        Closes the connection to the DuckDB database.
        """
        try:
            self.connection.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
