# Exercise 2.5.1: Database setup

This script creates the training database, loads CSV files, and checks that the records match up.

## Run it

You need Python 3.10 or newer. No extra packages are needed for the local SQLite version.

Put the CSV files and `starter_database.sql` in the same folder as `seed_database.py`. From that folder, run:

```bash
python seed_database.py
```

This creates `complaints_training.db`. The ZIP also includes `seeded_database.db`, which is a copy of a successful run for inspection. If you already ran the script and want to start over, run:

```bash
python seed_database.py --reset
```

`--reset` deletes and recreates the five training tables. Do not use it on a database you need to keep.

## Expected output

The output should end with `Integrity checks passed`.

| Table | Rows |
|---|---:|
| customers | 100 |
| accounts | 150 |
| complaints | 120 |
| service_requests | 5 |

The script also creates:

- `seed_run_log.txt`: what was loaded or why the run stopped.
- `integrity_report.txt`: counts and checks for missing or mismatched records.
- `rejected_rows.csv`: input problems, with the file and row number. It has only a header if nothing was rejected.

**About the data:** `customers.csv` and `accounts.csv` came with this exercise. `complaints.csv` is the 120-row file from Exercise 2.4.1. The five rows in `service_requests.csv` are **example data added for this exercise**, because a matching service-request CSV was not provided. Replace them if you receive the official file. `banking_complaint_scenarios.csv` contains 20 classification examples and is not loaded into this database.

The script reads the five CREATE TABLE statements from `starter_database.sql`. It does **not** run that file's INSERT statements, which only contain part of the data. All inserts come from the CSV files.

## PostgreSQL option

If you want to use PostgreSQL instead of a local SQLite file:

1. Create an empty PostgreSQL database, such as `complaints_training`.
2. Install the driver with `pip install -r requirements.txt`.
3. Set `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` in your environment. Do not put real passwords in Git.
4. Run `python seed_database.py --backend postgres`.

Use `--backend postgres --reset` only if you deliberately want to delete and recreate these training tables. A failed load is rolled back.

PostgreSQL follows the supplied schema as written. The bundled SQLite database is for local testing. PostgreSQL has not been tested against a live server here.

## Troubleshooting

- **Missing file or column:** Check the filename and the header shown in `rejected_rows.csv`.
- **Invalid customer or account:** Check that its ID exists in the related CSV. A complaint's account must belong to the same customer.
- **Tables already exist:** Use `--reset` only if you want to replace the data.
- **PostgreSQL connection fails:** Check the server, database name, and environment settings.

The script checks everything before inserting. If any row fails validation, it stops rather than loading part of the data. If loading fails during the database transaction, it rolls back.

## Test it

```bash
python -m unittest discover -s tests -v
```

The tests use temporary SQLite databases, not your training database.

**Project note:** The schema supplied for this exercise has plural table names (`customers`, `accounts`, `complaints`). The repositories created in Exercise 2.4.2 used singular table names (`customer`, `account`, `complaint`) and different columns, so those repositories will need to be updated before using this database. Do not point them at this database unchanged.

Exercise 2.5.2 can use this script and these setup instructions to recreate the environment.

No independent reviewer has run the setup instructions yet. The automated tests use fresh temporary folders.
