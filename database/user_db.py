"""
User database.

Handles user authentication and account management.
"""

import sqlite3
from pathlib import Path

import bcrypt

DATABASE_PATH = Path("database/chatbot.db")


class UserDatabase:
    """
    SQLite database for user accounts.
    """

    def __init__(
        self,
        database_path: Path = DATABASE_PATH,
    ) -> None:
        """
        Initialize the database.
        """

        self.database_path = database_path

        self._create_table()

        self._create_demo_user()

    def _create_table(self) -> None:
        """
        Create the users table.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password_hash TEXT,
                    created_at TEXT
                )
                """
            )

            connection.commit()

    def _hash_password(
        self,
        password: str,
    ) -> str:
        """
        Hash a password.
        """

        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt(),
        ).decode()

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verify a password.
        """

        return bcrypt.checkpw(
            password.encode(),
            password_hash.encode(),
        )

    def _create_demo_user(self) -> None:
        """
        Create demo account.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                """,
                ("demo",),
            )

            if cursor.fetchone():
                return

            cursor.execute(
                """
                INSERT INTO users (
                    username,
                    password_hash,
                    created_at
                )
                VALUES (?, ?, datetime('now'))
                """,
                (
                    "demo",
                    self._hash_password("demo123"),
                ),
            )

            connection.commit()


    def create_user(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Create a new user account.
        """

        try:

            with sqlite3.connect(self.database_path) as connection:

                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO users (
                        username,
                        password_hash,
                        created_at
                    )
                    VALUES (?, ?, datetime('now'))
                    """,
                    (
                        username,
                        self._hash_password(password),
                    ),
                )

                connection.commit()

            return True

        except sqlite3.IntegrityError:
            return False
        
    
    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> int | None:
        """
        Authenticate a user.

        Returns the user ID if successful,
        otherwise None.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    password_hash
                FROM users
                WHERE username = ?
                """,
                (username,),
            )

            result = cursor.fetchone()

        if result is None:
            return None

        user_id, password_hash = result

        if self.verify_password(
            password,
            password_hash,
        ):
            return user_id

        return None
    

    def get_username(
        self,
        user_id: int,
    ) -> str | None:
        """
        Return the username for a user ID.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT username
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            )

            result = cursor.fetchone()

        return result[0] if result else None