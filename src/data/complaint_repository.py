"""Read and create complaints. Business approval rules belong elsewhere."""
COLUMNS = ('complaint_id','customer_id','account_id','channel','category',
           'complaint_text','priority','status','received_at','assigned_analyst_id')

class ComplaintRepository:
    def __init__(self, db): self.db = db

    def get_by_id(self, complaint_id):
        with self.db.connection() as con:
            row = con.execute('SELECT * FROM complaint WHERE complaint_id = ?',
                              (complaint_id,)).fetchone()
            return dict(row) if row else None

    def get_for_customer(self, customer_id):
        with self.db.connection() as con:
            rows = con.execute('SELECT * FROM complaint WHERE customer_id = ? ORDER BY complaint_id',
                               (customer_id,)).fetchall()
            return [dict(r) for r in rows]

    def create(self, complaint):
        missing = [c for c in COLUMNS if c not in complaint]
        if missing:
            raise ValueError('Missing fields: ' + ', '.join(missing))
        with self.db.connection() as con:
            con.execute('INSERT INTO complaint (' + ','.join(COLUMNS) + ') VALUES (' +
                        ','.join('?' for _ in COLUMNS) + ')',
                        [complaint[c] for c in COLUMNS])
            row = con.execute('SELECT * FROM complaint WHERE complaint_id = ?',
                              (complaint['complaint_id'],)).fetchone()
            return dict(row)
