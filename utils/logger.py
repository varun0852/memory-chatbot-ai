"""
Application Logger

Centralized logging configuration used across
the entire application.
"""

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("MemoryChatBotAI")