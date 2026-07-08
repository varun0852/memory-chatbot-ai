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

    def __init__(self) -> None:
        """
        Initialize the database.
        """

        self._create_table()

    def _create_table(self) -> None:
        """
        Create the conversations table if it does not exist.
        """

        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE,
                    title TEXT,
                    created_at TEXT,
                    messages TEXT,
                    total_exports INTEGER DEFAULT 0
                )
                """)

            connection.commit()

    def save_conversation(
        self,
        session_id: str,
        title: str,
        created_at: str,
        messages: list,
    ) -> None:
        """
        Save or update a conversation.
        """

        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO conversations (
                    session_id,
                    title,
                    created_at,
                    messages,
                    total_exports
                )
                VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    COALESCE(
                        (
                            SELECT total_exports
                            FROM conversations
                            WHERE session_id = ?
                        ),
                        0
                    )
                )
                """,
                (
                    session_id,
                    title,
                    created_at,
                    json.dumps(messages),
                    session_id,
                ),
            )

            connection.commit()

    def get_conversations(self) -> list:
        """
        Return all conversations ordered by newest first.
        """

        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    session_id,
                    title,
                    created_at
                FROM conversations
                ORDER BY created_at DESC
                """)

            return cursor.fetchall()

    def load_conversation(
        self,
        session_id: str,
    ) -> list:
        """
        Load a conversation by session ID.
        """

        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT messages
                FROM conversations
                WHERE session_id = ?
                """,
                (session_id,),
            )

            result = cursor.fetchone()

        if result is None:
            return []

        return json.loads(result[0])

    def delete_conversation(
        self,
        session_id: str,
    ) -> None:
        """
        Delete a conversation.
        """

        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM conversations
                WHERE session_id = ?
                """,
                (session_id,),
            )

            connection.commit()

    def increment_export_count(
        self,
        session_id: str,
    ) -> None:
        """
        Increment the export count.
        """

        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE conversations
                SET total_exports = total_exports + 1
                WHERE session_id = ?
                """,
                (session_id,),
            )

            connection.commit()

    def search_conversations(
        self,
        query: str,
    ) -> list:
        """
        Search conversations by title.
        """

        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    session_id,
                    title,
                    created_at
                FROM conversations
                WHERE
                    title LIKE ?
                    OR messages LIKE ?
                ORDER BY created_at DESC
                """,
                (
                    f"%{query}%",
                    f"%{query}%",
                ),
            )

            return cursor.fetchall()

    def get_statistics(self) -> dict:
        """
        Return conversation statistics.
        """

        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    messages,
                    total_exports
                FROM conversations
                """)

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
            total_messages / total_conversations if total_conversations > 0 else 0
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
