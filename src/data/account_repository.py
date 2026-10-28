"""Read accounts that belong to a customer."""

from src.data.records import all_records


class AccountRepository:
    def __init__(self, db):
        self.db = db

    def get_for_customer(self, customer_id):
        with self.db.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT account_id, customer_id, account_number,
                              account_type, status, current_balance, opened_date
                       FROM account
                       WHERE customer_id = %s
                       ORDER BY account_id""",
                    (customer_id,),
                )
                return all_records(cursor)  # Empty list if none found
