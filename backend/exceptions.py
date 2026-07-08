"""
Custom exceptions used by the chatbot backend.
"""


class ChatBotError(Exception):
    """Base exception for chatbot-related errors."""

    pass


class InvalidAPIKeyError(ChatBotError):
    """Raised when the API key is missing or invalid."""

    pass


class APIConnectionError(ChatBotError):
    """Raised when the chatbot cannot connect to the API."""

    pass


class APITimeoutError(ChatBotError):
    """Raised when the API request times out."""

    pass


class RateLimitError(ChatBotError):
    """Raised when the API rate limit is exceeded."""

    pass


class ResponseError(ChatBotError):
    """Raised when the API returns an invalid response."""

    pass
