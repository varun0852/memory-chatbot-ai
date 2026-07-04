"""
Data models used by the chatbot.
"""

from typing import TypedDict


class ChatMessage(TypedDict):
    """
    Represents a single chat message.
    """

    role: str
    content: str
    timestamp: str