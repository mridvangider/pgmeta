import os
import pytest

from pgmeta import PgMetaClient



@pytest.fixture
def client():
    """Create a PgMetaClient instance with real PostgreSQL connection."""
    host = os.environ["PGMETA_HOST"]
    port = int(os.environ["PGMETA_PORT"])
    user = os.environ["PGMETA_USER"]
    password = os.environ["PGMETA_PASSWORD"]
    db = os.environ["PGMETA_DATABASE"]

    client = PgMetaClient(
        host=host,
        port=port,
        user=user,
        password=password,
        db=db
    )
    client.connect()
    yield client
    client.close()


def test_get_all_databases(client):
    """Test that get_all_databases returns database list."""
    databases = client.get_all_databases()
    assert isinstance(databases, list)
    for db in databases:
        assert "datname" in db


def test_get_all_schemas(client):
    """Test that get_all_schemas returns schema list."""
    schemas = client.get_all_schemas()
    assert isinstance(schemas, list)
    for schema in schemas:
        assert "schema_name" in schema


def test_get_all_tables_with_schema(client):
    """Test that get_all_tables with schema filter works."""
    tables = client.get_all_tables("public")
    assert isinstance(tables, list)
    for table in tables:
        assert "table_name" in table


def test_get_all_tables_without_schema(client):
    """Test that get_all_tables without schema returns all tables."""
    tables = client.get_all_tables()
    assert isinstance(tables, list)
    for table in tables:
        assert "table_name" in table


def test_get_all_columns_with_schema(client):
    """Test that get_all_columns with schema filter works."""
    columns = client.get_all_columns("public")
    assert isinstance(columns, list)
    for col in columns:
        assert "column_name" in col
        assert "data_type" in col


def test_get_all_columns_without_table(client):
    """Test that get_all_columns without table returns all columns in database."""
    columns = client.get_all_columns()
    assert isinstance(columns, list)
    for col in columns:
        assert "column_name" in col
        assert "data_type" in col


def test_get_all_columns_with_schema_and_table(client):
    """Test that get_all_columns filters by both schema and table."""
    columns = client.get_all_columns("public", "pg_catalog.pg_database")
    assert isinstance(columns, list)
    for col in columns:
        assert "column_name" in col
        assert "data_type" in col


def test_change_db(client):
    """Test that change_db switches connection to different database."""
    original_db = client._db
    new_db = os.getenv("PGMETA_DEFAULT_DATABASE") or "postgres"
    client.change_db(new_db)
    assert client._db == new_db
    client.change_db(original_db)


def test_close_explicit(client):
    """Test that explicit close closes the connection and cursor."""
    original_conn = client._connection
    original_cursor = client._cursor
    client.close()
    assert original_conn is not None
    assert original_cursor is not None
    assert client._connection is None
    assert client._cursor is None


def test_context_manager(client):
    """Test that PgMetaClient works as a context manager."""
    with client as c:
        assert c._connection is not None
        assert c._cursor is not None
    # After exit, connection should be closed
    assert client._connection is None
    assert client._cursor is None


def test_connect():
    """Test that connect establishes a new connection."""
    with PgMetaClient(
        host = os.environ["PGMETA_HOST"],
        port = int(os.environ["PGMETA_PORT"]),
        user = os.environ["PGMETA_USER"],
        password = os.environ["PGMETA_PASSWORD"],
        db = os.environ["PGMETA_DATABASE"]
    ) as client:
        assert client._connection is not None
        assert client._cursor is not None

