# Banking Complaint Resolution Project

A Python and SQLite project for managing and analyzing banking complaints. Includes SQL queries, database repositories, domain models, business services, and automated tests.

## Setup

Requires Python 3.10 or newer.

Open PowerShell in the project folder and run:

```powershell
python setup_local.py
python -m pip install pytest
python -m pytest tests -q
python -m unittest discover -s bulk/tests -v
```

Or double-click `setup_windows.bat` for the original setup and tests.

## Databases

| Database | Description |
|---|---|
| `data/original.db` | 30 complaints, used for SQL and repositories |
| `data/bulk.db` | 120 complaints, used for Python analysis and seeding |

These datasets are separate and use different table names.

## Project Structure

| Folder | Purpose |
|---|---|
| `legacy/` | SQL exercises, schema, and original data |
| `bulk/` | Larger dataset and database seeder |
| `analysis/` | Python complaint analysis |
| `src/data/` | Database connections and repositories |
| `src/domain/` | Domain models and validation |
| `src/services/` | Complaint business logic |
| `retrieval/` | SQL, RAG, and tool decisions |
| `tests/` | Automated tests |
| `docs/` | Documentation and test results |
| `reference/` | Exercise instructions |
| `data/` | SQLite databases |

## Useful Commands

```powershell
python setup_local.py          # Set up databases
python setup_local.py --reset  # Recreate databases
python -m src.demo             # Run repository demo
python -m src.services.demo    # Run service demo
python -m pytest tests -q      # Run main tests
```
