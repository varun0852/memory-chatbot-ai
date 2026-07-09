"""
Application Logger.

Centralized logging configuration used across
the entire application.
"""

from pathlib import Path
import logging

from config import LOG_FILE, LOG_FORMAT, LOG_LEVEL

# ==========================================================
# Ensure the log directory exists
# ==========================================================

Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Configure logging
# ==========================================================

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        ),
    ],
)

logger = logging.getLogger("MemoryChatBotAI")