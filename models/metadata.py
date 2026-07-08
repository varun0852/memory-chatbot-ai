"""
Data models used for conversation metadata.
"""

from typing import TypedDict


class ConversationMetadata(TypedDict):
    """
    Represents metadata for an exported conversation.
    """

    conversation_id: str
    exported_on: str
