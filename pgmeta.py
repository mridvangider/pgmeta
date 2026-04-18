import psycopg
from psycopg.rows import DictRow, dict_row
from urllib.parse import quote

class PgMetaClient:
    """PostgreSQL metadata client for retrieving database information."""

    def __init__(self, host: str, user: str, password: str, db: str = "postgres", port: int = 5432):
        """Initialize the PostgreSQL metadata client.

        Args:
            host: Database hostname or IP address
            user: Database username
            password: Database password
            db: Default database name (default: "postgres")
            port: Database port number (default: 5432)
        """
        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._db: str = db
        self._connection_string: str = f"postgres://{self._user}:{quote(self._password)}@{self._host}:{self._port}/{self._db}"
        self._connection: psycopg.Connection[DictRow] = psycopg.Connection[DictRow].connect(self._connection_string, row_factory=dict_row)
        self._cursor = self._connection.cursor()

    def is_connected(self):
        return not self._connection.closed \
            and not self._cursor.closed

    def connect(self, reconnect: bool = False):
        """Establish a new database connection."""
        if self.is_connected() and not reconnect:
            return
        
        self._connection_string: str = f"postgres://{self._user}:{quote(self._password)}@{self._host}:{self._port}/{self._db}"
        self._connection: psycopg.Connection[DictRow] = psycopg.Connection[DictRow].connect(self._connection_string, row_factory=dict_row)
        self._cursor = self._connection.cursor()

    def change_db(self, db: str):
        """Change the current database connection.

        Args:
            db: New database name to connect to
        """
        if db != self._db:
            self._db = db
            self.connect(reconnect=True)

    def close(self):
        """Close the database connection and self._cursor."""
        if self._cursor:
            self._cursor.close()
        if self._connection and not self._connection.closed:
            self._connection.close()

    def __enter__(self):
        """Enter the runtime context for the database connection."""
        if not self.is_connected():
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context and close the connection."""
        self.close()
        return False

    def get_all_databases(self) -> list[dict]:
        """Return all databases excluding templates.

        Returns:
            List of dictionaries containing database information from pg_database
        """
        if not self._cursor:
            self._cursor = self._connection.cursor()
        
        _ = self._cursor.execute("SELECT * FROM pg_database WHERE datistemplate = false")
        return self._cursor.fetchall()

    def get_all_schemas(self) -> list[dict]:
        """Return all schemas in the current database.

        Returns:
            List of dictionaries containing schema information from information_schema.schemata
        """
        if not self._cursor:
            self._cursor = self._connection.cursor()
        
        _ = self._cursor.execute("SELECT * FROM information_schema.schemata WHERE catalog_name = %s AND schema_name NOT IN ('pg_catalog', 'information_schema')", (self._db,))
        return self._cursor.fetchall()

    def get_all_tables(self, schema: str | None = None) -> list[dict]:
        """Return all tables in the database.

        Args:
            schema: Optional schema name to filter tables by

        Returns:
            List of dictionaries containing table information from information_schema.tables
        """
        if not self._cursor:
            self._cursor = self._connection.cursor()
        
        if schema:
            _ = self._cursor.execute("SELECT * FROM information_schema.tables WHERE table_schema = %s", (schema,))
        else:
            _ = self._cursor.execute("SELECT * FROM information_schema.tables")
        
        return self._cursor.fetchall()

    def get_all_columns(self, schema: str | None = None, table: str | None = None) -> list[dict]:
        """Return all columns in the database.

        Args:
            schema: Optional schema name to filter columns by
            table: Optional table name to filter columns by

        Returns:
            List of dictionaries containing column information from information_schema.columns
        """
        if not self._cursor:
            self._cursor = self._connection.cursor()
        
        cols_query = "SELECT * FROM information_schema.columns"
        conditions = []
        params = []
        if schema:
            conditions.append("table_schema = %s")
            params.append(schema)
        if table:
            conditions.append("table_name = %s")
            params.append(table)
        if conditions:
            cols_query += " WHERE " + " AND ".join(conditions)
            _ = self._cursor.execute(cols_query, tuple(params))
        else:
            _ = self._cursor.execute(cols_query)
        return self._cursor.fetchall()
