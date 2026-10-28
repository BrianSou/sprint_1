# Exercise 2.4.2: Database repositories

These files keep database queries in one place. Other parts of the project can call a repository instead of writing SQL themselves.

## Files

- `src/data/database_manager.py`: connects to PostgreSQL, commits successful work, rolls back failed work and closes connections.
- `src/data/customer_repository.py`: finds one customer by ID.
- `src/data/account_repository.py`: lists a customer's accounts.
- `src/data/complaint_repository.py`: finds complaints and creates a complaint.
- `src/data/records.py`: converts database rows into dictionaries.
- `tests/test_repositories.py`: tests reads, inserts, missing records and errors.

## Set up

1. Use the PostgreSQL database from Exercise 2.1.1. The queries use the `customer`, `account` and `complaint` tables.
2. Install the driver: `pip install -r requirements.txt`.
3. Set `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASSWORD` as environment variables. See `environment_example.txt` for the names. Use your actual database values, not `replace_me`.
4. Keep passwords out of Python files and Git. `MODEL_API_KEY` is not used in this exercise.

For example, in a Linux or macOS terminal:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=complaints_training
export DB_USER=training_user
# Set DB_PASSWORD privately in your terminal environment.
```

## Example calls

Run this from the project root after configuring the database:

```python
from src.data.database_manager import DatabaseManager
from src.data.customer_repository import CustomerRepository
from src.data.account_repository import AccountRepository
from src.data.complaint_repository import ComplaintRepository

db = DatabaseManager()

customer = CustomerRepository(db).get_by_id("CUS001")
accounts = AccountRepository(db).get_for_customer("CUS001")
complaint = ComplaintRepository(db).get_by_id("CMP001")
customer_complaints = ComplaintRepository(db).get_for_customer("CUS001")
print(customer, accounts, complaint, customer_complaints)
```

To create a complaint, pass a dictionary with the 10 fields from the `complaint` table. The repository will not decide the status or priority for you.

```python
new_complaint = {
    "complaint_id": "CMP100",
    "customer_id": "CUS001",
    "account_id": "ACC001",
    "channel": "Email",
    "category": "Fee Dispute",
    "complaint_text": "Unexpected charge",
    "priority": "Medium",
    "status": "OPEN",
    "received_at": "2026-10-27 10:00:00",
    "assigned_analyst_id": None,
}
saved = ComplaintRepository(db).create(new_complaint)
```

Lookups return a dictionary or `None`. List methods return a list, or `[]` if nothing matches. `create()` returns the new complaint. Database errors are raised to the caller after rollback.

## Where SQL belongs

SQL belongs in the repository files under `src/data/`. Services, APIs and agents should call repository methods instead of writing their own SQL. The database manager only handles connections and transactions. Business decisions, such as when to escalate a complaint, belong outside the repositories.

All values passed to SQL use `%s` placeholders. No user input is added directly to a query string.

## Run the tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

The tests use a temporary SQLite database with the same key columns. They run without a PostgreSQL server or passwords. The test adapter changes PostgreSQL `%s` placeholders to SQLite `?` placeholders. Production queries still use PostgreSQL placeholders.

## Notes

- Table and column names are based on the `customer.csv`, `account.csv` and `complaint.csv` files supplied for the earlier SQL exercises. Compare them with your actual Exercise 2.1.1 database schema before connecting.
- I could not verify a live PostgreSQL connection because no server or credentials were supplied. The tests cover repository behavior locally, not PostgreSQL integration.
- These repositories do not check customer ownership or decide who can access a record. The service/API layer needs authorization checks before using them.
- Exercise 2.5.1 can reuse the connection and validation patterns. Week 3 services can use the repository methods.
