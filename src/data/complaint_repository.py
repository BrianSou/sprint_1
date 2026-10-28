"""Look up complaints and save new complaints."""

from src.data.records import all_records, one_record


COLUMNS = (
    "complaint_id", "customer_id", "account_id", "channel", "category",
    "complaint_text", "priority", "status", "received_at", "assigned_analyst_id",
)


class ComplaintRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, complaint_id):
        with self.db.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT complaint_id, customer_id, account_id, channel,
                              category, complaint_text, priority, status,
                              received_at, assigned_analyst_id
                       FROM complaint
                       WHERE complaint_id = %s""",
                    (complaint_id,),
                )
                return one_record(cursor)

    def get_for_customer(self, customer_id):
        with self.db.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT complaint_id, customer_id, account_id, channel,
                              category, complaint_text, priority, status,
                              received_at, assigned_analyst_id
                       FROM complaint
                       WHERE customer_id = %s
                       ORDER BY complaint_id""",
                    (customer_id,),
                )
                return all_records(cursor)

    def create(self, complaint):
        # The caller chooses status, priority and other values.
        # This repository only saves them.
        missing = [name for name in COLUMNS if name not in complaint]
        if missing:
            raise ValueError("Missing complaint fields: " + ", ".join(missing))

        with self.db.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO complaint (
                           complaint_id, customer_id, account_id, channel, category,
                           complaint_text, priority, status, received_at, assigned_analyst_id
                       ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       RETURNING complaint_id, customer_id, account_id, channel,
                                 category, complaint_text, priority, status,
                                 received_at, assigned_analyst_id""",
                    tuple(complaint[name] for name in COLUMNS),
                )
                return one_record(cursor)
