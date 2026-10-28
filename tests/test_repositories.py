"""Repository tests with a small, temporary database."""

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.data.database_manager import DatabaseManager
from src.data.customer_repository import CustomerRepository
from src.data.account_repository import AccountRepository
from src.data.complaint_repository import ComplaintRepository


# SQLite uses ? instead of PostgreSQL's %s. Only the test cursor changes this.
class TestCursor(sqlite3.Cursor):
    def execute(self, sql, parameters=()):
        return super().execute(sql.replace("%s", "?"), parameters)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class TestConnection(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.was_closed = False

    def cursor(self):
        return super().cursor(factory=TestCursor)

    def close(self):
        self.was_closed = True
        super().close()


NEW_COMPLAINT = {
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


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.db_path = Path(self.folder.name) / "test.db"
        self.connections = []

        def connect():
            connection = sqlite3.connect(self.db_path, factory=TestConnection)
            connection.execute("PRAGMA foreign_keys = ON")
            self.connections.append(connection)
            return connection

        self.db = DatabaseManager(connector=connect)
        with self.db.connection() as connection:
            connection.executescript("""
                CREATE TABLE customer (
                    customer_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT,
                    email TEXT, phone_number TEXT, segment TEXT, date_created TEXT
                );
                CREATE TABLE account (
                    account_id TEXT PRIMARY KEY, customer_id TEXT REFERENCES customer(customer_id),
                    account_number TEXT, account_type TEXT, status TEXT,
                    current_balance REAL, opened_date TEXT
                );
                CREATE TABLE complaint (
                    complaint_id TEXT PRIMARY KEY, customer_id TEXT REFERENCES customer(customer_id),
                    account_id TEXT REFERENCES account(account_id), channel TEXT,
                    category TEXT, complaint_text TEXT, priority TEXT, status TEXT,
                    received_at TEXT, assigned_analyst_id TEXT
                );
                INSERT INTO customer VALUES
                    ('CUS001', 'Sam', 'Lee', 'sam@example.test', '5551000', 'Retail', '2026-01-01'),
                    ('CUS002', 'Alex', 'Kim', 'alex@example.test', '5552000', 'Retail', '2026-01-02');
                INSERT INTO account VALUES
                    ('ACC001', 'CUS001', '10001', 'Chequing', 'ACTIVE', 125.50, '2026-01-01'),
                    ('ACC002', 'CUS001', '10002', 'Savings', 'ACTIVE', 350.00, '2026-01-02');
                INSERT INTO complaint VALUES
                    ('CMP001', 'CUS001', 'ACC001', 'Email', 'Fee Dispute',
                     'Unexpected fee', 'High', 'OPEN', '2026-01-05', NULL),
                    ('CMP002', 'CUS001', 'ACC002', 'Phone', 'Service Delay',
                     'Slow service', 'Medium', 'CLOSED', '2026-01-07', NULL);
            """)

    def tearDown(self):
        self.folder.cleanup()

    def test_customer_found(self):
        customer = CustomerRepository(self.db).get_by_id("CUS001")
        self.assertEqual(customer["first_name"], "Sam")

    def test_customer_not_found(self):
        self.assertIsNone(CustomerRepository(self.db).get_by_id("CUS999"))

    def test_accounts_for_customer(self):
        accounts = AccountRepository(self.db).get_for_customer("CUS001")
        self.assertEqual([a["account_id"] for a in accounts], ["ACC001", "ACC002"])

    def test_no_accounts_returns_empty_list(self):
        self.assertEqual(AccountRepository(self.db).get_for_customer("CUS002"), [])

    def test_complaint_found(self):
        complaint = ComplaintRepository(self.db).get_by_id("CMP001")
        self.assertEqual(complaint["status"], "OPEN")

    def test_complaint_not_found(self):
        self.assertIsNone(ComplaintRepository(self.db).get_by_id("CMP999"))

    def test_complaints_for_customer(self):
        complaints = ComplaintRepository(self.db).get_for_customer("CUS001")
        self.assertEqual(len(complaints), 2)

    def test_no_complaints_returns_empty_list(self):
        self.assertEqual(ComplaintRepository(self.db).get_for_customer("CUS002"), [])

    def test_create_complaint(self):
        saved = ComplaintRepository(self.db).create(NEW_COMPLAINT)
        self.assertEqual(saved["complaint_id"], "CMP100")
        self.assertEqual(saved["priority"], "Medium")
        self.assertEqual(ComplaintRepository(self.db).get_by_id("CMP100")["status"], "OPEN")

    def test_create_requires_all_fields(self):
        with self.assertRaisesRegex(ValueError, "Missing complaint fields"):
            ComplaintRepository(self.db).create({"complaint_id": "CMP100"})

    def test_duplicate_id_fails_and_closes_connection(self):
        with self.assertRaises(sqlite3.IntegrityError):
            ComplaintRepository(self.db).create({**NEW_COMPLAINT, "complaint_id": "CMP001"})
        self.assertTrue(self.connections[-1].was_closed)
        self.assertEqual(ComplaintRepository(self.db).get_by_id("CMP001")["category"], "Fee Dispute")

    def test_sql_injection_text_is_not_executed(self):
        value = "CUS001' OR '1'='1"
        self.assertIsNone(CustomerRepository(self.db).get_by_id(value))
        self.assertEqual(len(AccountRepository(self.db).get_for_customer("CUS001")), 2)

    def test_rollback_on_error(self):
        with self.assertRaisesRegex(RuntimeError, "test failure"):
            with self.db.connection() as connection:
                connection.execute("INSERT INTO customer (customer_id) VALUES ('CUS200')")
                raise RuntimeError("test failure")
        self.assertTrue(self.connections[-1].was_closed)
        self.assertIsNone(CustomerRepository(self.db).get_by_id("CUS200"))

    def test_success_also_closes_connection(self):
        CustomerRepository(self.db).get_by_id("CUS001")
        self.assertTrue(self.connections[-1].was_closed)

    def test_read_error_closes_connection(self):
        with self.db.connection() as connection:
            connection.execute("ALTER TABLE account RENAME COLUMN account_type TO renamed_type")
        with self.assertRaises(sqlite3.OperationalError):
            AccountRepository(self.db).get_for_customer("CUS001")
        self.assertTrue(self.connections[-1].was_closed)

    def test_missing_environment_settings(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "Missing database settings"):
                DatabaseManager._connect_postgres()

    def test_invalid_port_setting(self):
        settings = dict(DB_HOST="localhost", DB_PORT="not-a-number", DB_NAME="test",
                        DB_USER="test", DB_PASSWORD="test")
        with patch.dict(os.environ, settings, clear=True):
            with self.assertRaisesRegex(ValueError, "DB_PORT"):
                DatabaseManager._connect_postgres()


if __name__ == "__main__":
    unittest.main()
