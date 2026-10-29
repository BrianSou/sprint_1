"""Open, commit, roll back, and close SQLite connections."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parents[2] / 'data' / 'original.db'

class DatabaseManager:
    def __init__(self, db_path=DEFAULT_DB):
        self.db_path = Path(db_path)

    @contextmanager
    def connection(self):
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA foreign_keys = ON')
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()
