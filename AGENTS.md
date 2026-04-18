# AGENTS.md

## Testing

Tests require a running PostgreSQL database. Set these environment variables before running tests:

```bash
export PGMETA_HOST=localhost
export PGMETA_PORT=5432
export PGMETA_USER=postgres
export PGMETA_PASSWORD=your_password
export PGMETA_DATABASE=postgres
```

Run tests: `pytest`

## Linting

```bash
ruff check .
```

## Project Structure

- Single package: `pgmeta.py` exports `PgMetaClient`
- Entry point defined in `pyproject.toml`
- Tests in `tests/pgmeta_test.py`