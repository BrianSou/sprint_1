# Repository Test Results

Run from the project folder:

```bash
python -m unittest discover -s tests -v
```

Result: 17 tests passed.

I checked customer and complaint lookups, account lists, creating complaints, missing IDs, missing fields, duplicate IDs and SQL injection-style input. I also tested rollback after an error, missing environment settings, invalid ports and connection cleanup.

The tests used a temporary SQLite database, not the live PostgreSQL server. PostgreSQL connection and schema compatibility still need to be checked in the real training environment.
