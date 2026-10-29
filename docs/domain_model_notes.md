# Exercise 3.1.1: Domain model notes

## Model plan

- **Customer:** Holds a customer ID, name and optional email.
- **Account:** Holds an account ID, the owner customer ID, account type, status and optional balance.
- **Complaint:** Holds a complaint ID, customer ID, optional account ID, category, priority, status and optional received date.
- **ComplaintStatusEvent:** Records a status change, who made it and when.

The ID fields connect the objects. A complaint belongs to a customer, but it can have no account. An account belongs to a customer. Checking whether that account actually belongs to the complaint's customer still needs a database query or service-level check.

## Controlled values

I used Enums for complaint category, priority and status. This stops mistakes like `Hihg` or `WAITING` from being accepted.

The original Week 2 dataset has 7 categories, priorities Low/Medium/High/Critical, and statuses OPEN, IN_PROGRESS, UNDER_REVIEW and CLOSED. The separate bulk dataset has 6 more categories and the status Escalated. Both category lists are supported.

The bulk CSV uses `In Review`, which maps to `UNDER_REVIEW`. `Escalated` maps to `ESCALATED`. In the original database, an escalation decision is stored separately in `review_decision`; it is not automatically the complaint's status.

## Status transitions

| Current status | Allowed next statuses |
|---|---|
| New complaint | OPEN |
| OPEN | IN_PROGRESS, UNDER_REVIEW, ESCALATED |
| IN_PROGRESS | UNDER_REVIEW, ESCALATED, CLOSED |
| UNDER_REVIEW | IN_PROGRESS, ESCALATED, CLOSED |
| ESCALATED | IN_PROGRESS, UNDER_REVIEW, CLOSED |
| CLOSED | None |

A complaint cannot skip directly from OPEN to CLOSED, reopen after being CLOSED or change to the same status again. The model checks these rules before creating a status event.

**Note:** The exercise requires explicit transitions but does not give the bank's actual transition rules. These are reasonable training rules based partly on the Week 2 history. They need approval before being used as real business policy.

## Design choices

- I used `@dataclass` to keep the models small and typed.
- I made the models frozen so a caller cannot change a complaint status without using the provided method.
- `change_status()` returns a new complaint and its status event. It does not save either one to the database.
- Category, priority and status are validated. Missing required IDs and names are rejected.
- Money uses `Decimal` to avoid common floating point rounding problems.
- No SQL, database connections, web routes or API calls belong in these files. Repositories handle data access; Week 3 services will connect the repositories and these models.

## Testing

Run from the project root:

```powershell
python -m pip install pytest
python -m pytest tests/test_domain_models.py -v
```

Tests cover valid models, invalid category/priority/status, missing fields, allowed and blocked transitions, initial OPEN status, a completed complaint, and creation of a status event.

## Limitations

These models check values and transitions, not whether an ID really exists in the database. Dates from CSVs and SQL rows must be converted to `datetime` before passing them to the model. A service will also need to save the updated complaint and its event together in a database transaction. The approved Week 1 specification was not supplied, so the proposed transitions cannot yet be confirmed against it.
