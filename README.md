# Banking Complaint Exercises, Week 2

This repository contains working local versions of exercises 2.1.1 through 2.5.1.

## Quick start (Windows)

Install Python 3.10 or newer. Open PowerShell in this folder and run:

```powershell
python setup_local.py
python -m unittest discover -s tests -v
```

No packages or database server are needed for the SQLite version. Open the `.db` files with DBeaver if you want to inspect the tables. If `python` is not recognized, try `py` instead.

## What gets created

- `data/original.db` contains the **original banking complaint dataset**: 30 complaints and related customers, accounts, histories, reviews, and policies. Its tables have singular names such as `complaint` and `customer`. Exercises 2.1.1 through 2.3.2 and the repositories in 2.4.2 use this database.
- `data/bulk.db` contains the **120-complaint training dataset** from later exercises. Its tables use plural names such as `complaints` and `customers`. Exercises 2.4.1 and 2.5.1 use this dataset.

These are two different datasets. Do not mix their IDs or run one schema's queries against the other database.

## Useful commands

```powershell
python setup_local.py                 # create any missing databases and produce output reports
python setup_local.py --reset         # intentionally recreate both databases
python -m unittest discover -s tests -v
python -m unittest discover -s bulk/tests -v
python -m src.demo                    # sample calls to the repositories
```

For the bulk seeder alone:

```powershell
python bulk/seed_database.py --db data/bulk.db --data-dir bulk/data --reset
```

Do not run `--reset` on a database with changes you need to keep. It replaces the exercise data.

## Folder guide

| Folder | Purpose |
|---|---|
| `legacy/` | Original 16 CSVs, SQLite schema, joins, metrics, advanced SQL and evidence |
| `bulk/` | 120-complaint input CSVs, seeder and local analysis results |
| `analysis/` | Exercise 2.4.1 Python analysis and its input notes |
| `src/data/` | SQLite database manager and customer, account, complaint repositories |
| `retrieval/` | Exercise 2.3.2 decision matrix and design notes |
| `tests/` | Working repository and original seeding tests |
| `reference/` | Assignment documents and preserved earlier draft SQL |
| `data/` | Local `.db` files created by setup |

## Notes and limits

- The original 30-row `complaint.csv` has no complaint closure date. The original database cannot give a trustworthy average resolution time. The 120-row dataset has closure dates for this calculation.
- `bulk/data/service_requests.csv` contains five **example records** added in exercise 2.5.1 because no matching official service-request file was supplied for that dataset.
- The original `starter_database.sql` has partial INSERT examples. The bulk seeder uses only its CREATE TABLE statements and loads the full CSVs instead.
- The RAG/human approval exercise is a written design. There is no live retrieval or AI approval service in this Week 2 repository.
- The bulk seeder has an untested optional PostgreSQL path. The setup and tests here use SQLite.
- The extra data dictionary, joins, metrics and advanced SQL question sheets are now included under `reference/requirements/`. The approved Week 1 release is still missing. The original service-request CSV does not contain a complaint ID, so the requested complaint-to-service-request link cannot be verified. See `docs/REQUIREMENTS_CHECK.md`.

See `legacy/docs/`, `bulk/README_setup.md` and `docs/REPOSITORY_NOTES.md` for exercise-specific details.

## One-click Windows setup

You can also double-click `setup_windows.bat`. It runs setup and both sets of tests. See `docs/TEST_RESULTS.md` for the recorded checks.

## New reference files and checks

- `reference/requirements/` contains the newly provided question sheets and metric definitions.
- `docs/REQUIREMENTS_CHECK.md` lists what is covered and what remains outside the supplied data.
- `legacy/build_data_dictionary.py` rebuilds the column-by-column dictionary from the local database.
- `bulk/sql/closed_case_resolution.sql` calculates closed-case resolution time using the separate bulk database.
- `tests/test_requirements.py` checks the join questions, age bucket boundaries and data dictionary.
