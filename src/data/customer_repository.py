"""Read customer records."""

from src.data.records import one_record


class CustomerRepository:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, customer_id):
        with self.db.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT customer_id, first_name, last_name, email,
                              phone_number, segment, date_created
                       FROM customer
                       WHERE customer_id = %s""",
                    (customer_id,),
                )
                return one_record(cursor)  # None if no customer exists
