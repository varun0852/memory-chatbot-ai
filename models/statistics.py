"""
Data models used for conversation statistics.
"""

from typing import TypedDict


class ChatStatistics(TypedDict):
    """
    Represents statistics about a conversation.
    """

    message_count: int
    user_messages: int
    assistant_messages: int
    session_duration: str