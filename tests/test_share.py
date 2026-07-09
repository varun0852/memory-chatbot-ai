import json

from utils.share import (
    export_chat_package,
    import_chat_package,
)


def test_export_chat_package() -> None:
    """
    Test exporting a conversation package.
    """

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

    metadata = {
        "conversation_id": "abc123",
        "created_at": "2026-07-09",
        "exported_at": "2026-07-09",
        "model": "llama-3.3-70b",
    }

    package = export_chat_package(
        messages,
        metadata,
    )

    data = json.loads(package)

    assert data["version"] == "2.0"
    assert data["metadata"]["conversation_id"] == metadata["conversation_id"]

    assert data["metadata"]["created_at"] == metadata["created_at"]

    assert data["metadata"]["model"] == metadata["model"]

    assert (
        data["metadata"]["source_conversation_id"]
        == metadata["conversation_id"]
    )
    assert data["messages"] == messages
    assert data["messages"] == messages


def test_import_chat_package() -> None:
    """
    Test importing a valid conversation package.
    """

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

    metadata = {
        "conversation_id": "abc123",
        "created_at": "2026-07-09",
        "exported_at": "2026-07-09",
        "model": "llama-3.3-70b",
    }

    package = export_chat_package(
        messages,
        metadata,
    )

    imported_messages, imported_metadata = import_chat_package(
        package,
    )

    assert imported_messages == messages

    assert (
        imported_metadata["conversation_id"]
        == metadata["conversation_id"]
    )

    assert (
        imported_metadata["source_conversation_id"]
        == metadata["conversation_id"]
    )

    assert (
        imported_metadata["model"]
        == metadata["model"]
    )

import pytest


def test_import_invalid_json() -> None:
    """
    Test importing invalid JSON.
    """

    with pytest.raises(ValueError):
        import_chat_package(
            "This is not JSON",
        )

def test_import_missing_version() -> None:
    """
    Test importing a package without a version.
    """

    package = json.dumps(
        {
            "metadata": {},
            "messages": [],
        }
    )

    with pytest.raises(ValueError):
        import_chat_package(package)


def test_import_missing_metadata() -> None:
    """
    Test importing a package without metadata.
    """

    package = json.dumps(
        {
            "version": "2.0",
            "messages": [],
        }
    )

    with pytest.raises(ValueError):
        import_chat_package(package)

def test_import_missing_messages() -> None:
    """
    Test importing a package without messages.
    """

    package = json.dumps(
        {
            "version": "2.0",
            "metadata": {},
        }
    )

    with pytest.raises(ValueError):
        import_chat_package(package)

def test_import_invalid_structure() -> None:
    """
    Test importing a package with an invalid structure.
    """

    package = json.dumps(
        [
            "not",
            "a",
            "dictionary",
        ]
    )

    with pytest.raises(ValueError):
        import_chat_package(package)