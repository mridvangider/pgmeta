# pgmeta

PostgreSQL metadata client for retrieving database information.

## Installation

```bash
pip install pgmeta
```

## Usage

```python
from pgmeta import PgMetaClient

client = PgMetaClient(
    host="localhost",
    user="postgres",
    password="your_password",
    db="mydb"
)

# Get all databases
databases = client.get_all_databases()

# Get all schemas
schemas = client.get_all_schemas()

# Get all tables (optionally filtered by schema)
tables = client.get_all_tables(schema="public")

# Get all columns (optionally filtered by schema and table)
columns = client.get_all_columns(schema="public", table="users")

client.close()
```

## API

### PgMetaClient

#### `__init__(host, user, password, db="postgres", port=5432)`

Create a new PostgreSQL metadata client.

#### `get_all_databases() -> list[dict]`

Return all databases excluding templates.

#### `get_all_schemas() -> list[dict]`

Return all schemas in the current database.

#### `get_all_tables(schema: str | None = None) -> list[dict]`

Return all tables in the database. Optionally filter by schema.

#### `get_all_columns(schema: str | None = None, table: str | None = None) -> list[dict]`

Return all columns in the database. Optionally filter by schema and/or table.

## Development

```bash
# Install dependencies
uv sync

# Run tests
pytest

# Lint
ruff check .
```