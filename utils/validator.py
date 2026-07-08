"""
Input validation utilities for the chatbot.
"""

from config import MAX_PROMPT_LENGTH


def validate_prompt(prompt: str) -> None:
    """
    Validate a user prompt.

    Raises:
        ValueError: If the prompt is invalid.
    """

    if not prompt:
        raise ValueError("Prompt cannot be empty.")

    if not prompt.strip():
        raise ValueError("Prompt cannot contain only whitespace.")

    if len(prompt) > MAX_PROMPT_LENGTH:
        raise ValueError(f"Prompt cannot exceed {MAX_PROMPT_LENGTH} characters.")
