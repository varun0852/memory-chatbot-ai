"""
Application Logger

Centralized logging configuration used across
the entire application.
"""

import logging

from config import LOG_LEVEL, LOG_FORMAT, LOG_FILE

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger("MemoryChatBotAI")
