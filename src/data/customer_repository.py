"""Read customer records."""
class CustomerRepository:
    def __init__(self, db): self.db = db

    def get_by_id(self, customer_id):
        with self.db.connection() as con:
            row = con.execute('SELECT * FROM customer WHERE customer_id = ?',
                              (customer_id,)).fetchone()
            return dict(row) if row else None
