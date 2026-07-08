"""
Sharing utilities.

Provides helper functions for exporting and importing
Memory ChatBot conversation packages.
"""

import json

# Models
from models import ChatMessage
from models import ConversationMetadata


def export_chat_package(
    messages: list[ChatMessage],
    metadata: ConversationMetadata,
) -> str:
    """
    Export a conversation as a .chat package.
    """
    package = {
        "application": "Memory ChatBot AI",
        "version": "2.0",
        "metadata": {
            **metadata,
            "source_conversation_id": metadata["conversation_id"],
        },
        "messages": messages,
    }

    return json.dumps(
        package,
        indent=4,
        ensure_ascii=False,
    )


def import_chat_package(
    package: str,
) -> tuple[list[ChatMessage], ConversationMetadata]:
    """
    Import a conversation package.
    """
    # Validation

    # validation 1 no name change
    try:
        data = json.loads(package)

    except json.JSONDecodeError:
        raise ValueError("Invalid conversation package.")

    # validation 2 Application
    if data.get("application") != "Memory ChatBot AI":
        raise ValueError("This file was not created by Memory ChatBot AI.")

    # validation 3 Version
    if data.get("version") != "2.0":
        raise ValueError("Unsupported conversation version.")

    # Validation 4 Required Fields
    if "messages" not in data:
        raise ValueError("Conversation data is missing.")

    if "metadata" not in data:
        raise ValueError("Conversation metadata is missing.")

    return (
        data["messages"],
        data["metadata"],
    )
