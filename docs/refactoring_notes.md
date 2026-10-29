# Exercise 3.1.2: Refactoring notes

## Before

- The domain models checked values and status transitions, but they did not save data.
- Repositories could look up and create complaints, but did not handle status changes.
- A future API router would have needed to check customers, accounts and complaint status itself. That would repeat rules across different routes.

## After

- `ComplaintService` handles business rules such as checking customers, account ownership and status changes.
- `Complaint` and `ComplaintStatusEvent` handle validation and allowed transitions.
- The repositories contain the SQL. The service has no SQL.
- `dependencies.py` creates the real repositories. Tests can pass fake repositories instead.
- A status update and its history row are saved in one transaction. If writing history fails, the status update is rolled back.
- New complaints also get an initial `OPEN` history entry in the same transaction.

## Layers

| Layer | Job |
|---|---|
| Router (later) | Receive HTTP requests and return responses. FastAPI belongs here. |
| Service | Decide whether an operation is allowed and coordinate repositories. |
| Repository | Run parameterized SQL and save changes. |
| Domain | Define models and check their values and status rules. |
| Dependencies | Build the service with real or fake repositories. |

## Business rules used

1. The customer must exist before creating a complaint.
2. An account is optional. If supplied, it must belong to the customer.
3. New complaints always start with status `OPEN`.
4. Category and priority must match the domain enums.
5. Status changes must follow the transition rules in `src/domain/models.py`.
6. A `CLOSED` complaint cannot reopen under those rules.
7. The original Week 2 SQLite `complaint.status` column does not support `ESCALATED`. Escalation decisions are stored separately in `review_decision`, so the service rejects `ESCALATED` as a status in this database.

## Tests

Run:

```powershell
python -m pip install pytest
python -m pytest tests/test_complaint_service.py -v
```

The tests cover valid and missing records, duplicate IDs, wrong account ownership, bad category and priority, allowed and blocked status changes, fake repositories and database rollback after a failed history write.

## Limits

- These status transitions were proposed in Exercise 3.1.1. The bank's approved workflow rules were not provided.
- The service uses the original 30-complaint SQLite database, not the separate 120-complaint database.
- A valid `changed_by` value must refer to an existing employee when using the real SQLite repository. The database enforces this foreign key.
- Repository methods do not implement authorization. The future API will need to check who may view or change a complaint.
- This exercise does not implement FastAPI routes. Exercise 3.2.2 will call this service from the routes.
