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

    def execute_query(self, query: str) -> list:
        """
        Executes a query against the DuckDB database and returns the result.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            list: Results returned from the executed query
        """
        try:
            result = self.connection.execute(query).fetchall()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    def insert_data(self, table_name: str, data: pd.DataFrame) -> None:
        """
        Inserts data into a specific table in the DuckDB database.

        Args:
            table_name (str): The name of the table where the data will be inserted.
            data (pd.DataFrame): The data to be inserted. Must be a pandas DataFrame.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        try:
            self.connection.register("data_df", data)
            self.connection.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM data_df"
            )
            # If table exists, append data
            self.connection.execute(
                f"INSERT INTO {table_name} SELECT * FROM data_df"
            )
            self.connection.unregister("data_df")
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

    def get_tables(self) -> list:
        try:
            query = "SELECT table_name FROM information_schema.tables"
            result = self.connection.execute(query).fetchall()
            return [row[0] for row in result]
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
