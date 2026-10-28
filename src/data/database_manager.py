"""Database connection setup and cleanup."""

import os
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, connector=None):
        # Tests can pass a different connector instead of using PostgreSQL.
        self.connector = connector or self._connect_postgres

    @staticmethod
    def _connect_postgres():
        # Read settings from environment variables, not from the code.
        settings = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing = [name for name in settings if not os.getenv(name)]
        if missing:
            raise ValueError("Missing database settings: " + ", ".join(missing))

        try:
            port = int(os.environ["DB_PORT"])
            if not 1 <= port <= 65535:
                raise ValueError()
        except ValueError:
            raise ValueError("DB_PORT must be a valid port number") from None

        try:
            import psycopg2
        except ImportError:
            raise RuntimeError("Install the database driver: pip install -r requirements.txt") from None

        try:
            return psycopg2.connect(
                host=os.environ["DB_HOST"],
                port=port,
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=5,
            )
        except psycopg2.Error:
            # Show a useful error without exposing the password or connection string.
            raise ConnectionError("Database connection failed. Check the server and DB settings.") from None

    @contextmanager
    def connection(self):
        connection = self.connector()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
