from pathlib import Path

from database.conversation_db import ConversationDatabase

from pathlib import Path


def create_database(
    database_path: Path,
) -> ConversationDatabase:
    """
    Create a fresh database for testing.
    """

    return ConversationDatabase(
        database_path=database_path,
    )

def test_save_and_load_conversation(tmp_path: Path) -> None:
    """
    Test saving and loading a conversation.
    """

    db = create_database(
        tmp_path / "chatbot.db"
    )

    messages = [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hi!",
        },
    ]

    db.save_conversation(
        session_id="abc123",
        title="Test Chat",
        created_at="2026-07-09",
        messages=messages,
    )

    loaded = db.load_conversation("abc123")

    assert loaded == messages


def test_load_missing_conversation(
    tmp_path: Path,
) -> None:
    """
    Test loading a conversation that does not exist.
    """

    db = create_database(
        tmp_path / "chatbot.db"
    )

    conversation = db.load_conversation(
        "does_not_exist"
    )

    assert conversation == []


def test_delete_conversation(tmp_path: Path) -> None:
    """
    Test deleting a conversation.
    """

    db = create_database(
        tmp_path / "chatbot.db",
    )

    messages = [
        {
            "role": "user",
            "content": "Hello",
        }
    ]

    db.save_conversation(
        session_id="abc123",
        title="Test",
        created_at="2026-07-09",
        messages=messages,
    )

    db.delete_conversation("abc123")

    assert db.load_conversation("abc123") == []


def test_search_conversations(tmp_path: Path) -> None:
    """
    Test searching conversations.
    """

    db = create_database(
        tmp_path / "chatbot.db",
    )

    db.save_conversation(
        session_id="1",
        title="Python Tutorial",
        created_at="2026-07-09",
        messages=[],
    )

    db.save_conversation(
        session_id="2",
        title="Machine Learning",
        created_at="2026-07-09",
        messages=[],
    )

    results = db.search_conversations("Python")

    assert len(results) == 1
    assert results[0][1] == "Python Tutorial"


def test_get_conversations(tmp_path: Path) -> None:
    """
    Test retrieving all conversations.
    """

    db = create_database(
        tmp_path / "chatbot.db",
    )

    db.save_conversation(
        "1",
        "Chat One",
        "2026-07-09",
        [],
    )

    db.save_conversation(
        "2",
        "Chat Two",
        "2026-07-10",
        [],
    )

    conversations = db.get_conversations()

    assert len(conversations) == 2


def test_increment_export_count(tmp_path: Path) -> None:
    """
    Test incrementing export count.
    """

    db = create_database(
        tmp_path / "chatbot.db",
    )

    db.save_conversation(
        "1",
        "Test",
        "2026-07-09",
        [],
    )

    db.increment_export_count("1")
    db.increment_export_count("1")

    stats = db.get_statistics()

    assert stats["total_exports"] == 2


def test_get_statistics(tmp_path: Path) -> None:
    """
    Test conversation statistics.
    """

    db = create_database(
        tmp_path / "chatbot.db",
    )

    db.save_conversation(
        "1",
        "Chat One",
        "2026-07-09",
        [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ],
    )

    db.save_conversation(
        "2",
        "Chat Two",
        "2026-07-10",
        [
            {"role": "user", "content": "Question"},
            {"role": "assistant", "content": "Answer"},
            {"role": "user", "content": "Thanks"},
        ],
    )

    stats = db.get_statistics()

    assert stats["total_conversations"] == 2
    assert stats["total_messages"] == 5
    assert stats["user_messages"] == 3
    assert stats["assistant_messages"] == 2