"""
Custom exceptions used by the chatbot backend.
"""

class ChatBotError(Exception):
    """Base exception for chatbot-related errors."""
    pass


class InvalidAPIKeyError(ChatBotError):
    """Raised when the API key is missing or invalid."""
    pass