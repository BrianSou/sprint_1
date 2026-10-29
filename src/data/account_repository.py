"""Read a customer's accounts."""
class AccountRepository:
    def __init__(self, db): self.db = db

    def get_for_customer(self, customer_id):
        with self.db.connection() as con:
            rows = con.execute('SELECT * FROM account WHERE customer_id = ? ORDER BY account_id',
                               (customer_id,)).fetchall()
            return [dict(r) for r in rows]
