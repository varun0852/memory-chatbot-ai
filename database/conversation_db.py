"""
Conversation database.

Handles storing and retrieving chat conversations.
"""

import json
import sqlite3
from pathlib import Path

DATABASE_PATH = Path("database/chatbot.db")


class ConversationDatabase:
    """
    SQLite database for conversation storage.
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

    def _create_table(self) -> None:
        """
        Create the conversations table if it does not exist.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_id TEXT UNIQUE,
                    title TEXT,
                    created_at TEXT,
                    messages TEXT,
                    total_exports INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

            connection.commit()

    def save_conversation(
        self,
        user_id: int,
        session_id: str,
        title: str,
        created_at: str,
        messages: list,
    ) -> None:
        """
        Save or update a conversation.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT total_exports
                FROM conversations
                WHERE
                    user_id = ?
                    AND session_id = ?
                """,
                (
                    user_id,
                    session_id,
                ),
            )

            existing = cursor.fetchone()

            exports = existing[0] if existing else 0

            cursor.execute(
                """
                INSERT OR REPLACE INTO conversations (
                    user_id,
                    session_id,
                    title,
                    created_at,
                    messages,
                    total_exports
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    session_id,
                    title,
                    created_at,
                    json.dumps(messages),
                    exports,
                ),
            )

            connection.commit()

    def get_conversations(
        self,
        user_id: int,
    ) -> list:
        """
        Return all conversations for a user.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    session_id,
                    title,
                    created_at
                FROM conversations
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,),
            )

            return cursor.fetchall()

    def load_conversation(
        self,
        user_id: int,
        session_id: str,
    ) -> list:
        """
        Load a conversation.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT messages
                FROM conversations
                WHERE
                    user_id = ?
                    AND session_id = ?
                """,
                (
                    user_id,
                    session_id,
                ),
            )

            result = cursor.fetchone()

        if result is None:
            return []

        return json.loads(result[0])
    

    def delete_conversation(
        self,
        user_id: int,
        session_id: str,
    ) -> None:
        """
        Delete a conversation.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM conversations
                WHERE
                    user_id = ?
                    AND session_id = ?
                """,
                (
                    user_id,
                    session_id,
                ),
            )

            connection.commit()

    def increment_export_count(
        self,
        user_id: int,
        session_id: str,
    ) -> None:
        """
        Increment the export count.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE conversations
                SET total_exports = total_exports + 1
                WHERE
                    user_id = ?
                    AND session_id = ?
                """,
                (
                    user_id,
                    session_id,
                ),
            )

            connection.commit()

    def search_conversations(
        self,
        user_id: int,
        query: str,
    ) -> list:
        """
        Search conversations.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    session_id,
                    title,
                    created_at
                FROM conversations
                WHERE
                    user_id = ?
                    AND (
                        title LIKE ?
                        OR messages LIKE ?
                    )
                ORDER BY created_at DESC
                """,
                (
                    user_id,
                    f"%{query}%",
                    f"%{query}%",
                ),
            )

            return cursor.fetchall()

    def get_statistics(
        self,
        user_id: int,
    ) -> dict:
        """
        Return statistics for a single user.
        """

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    messages,
                    total_exports
                FROM conversations
                WHERE user_id = ?
                """,
                (user_id,),
            )

            conversations = cursor.fetchall()

        total_conversations = len(conversations)

        total_messages = 0
        user_messages = 0
        assistant_messages = 0
        total_exports = 0

        for messages_json, exports in conversations:

            messages = json.loads(messages_json)

            total_exports += exports

            for message in messages:

                total_messages += 1

                if message["role"] == "user":
                    user_messages += 1

                elif message["role"] == "assistant":
                    assistant_messages += 1

        average_messages = (
            total_messages / total_conversations
            if total_conversations > 0
            else 0
        )

        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "average_messages_per_conversation": round(
                average_messages,
                1,
            ),
            "total_exports": total_exports,
        }