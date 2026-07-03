"""
Application Configuration

This module loads environment variables and stores
all application-wide configuration in one place.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GROQ API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Llama Model
MODEL_NAME = "llama-3.3-70b-versatile"

# Temperature for response generation
TEMPERATURE = 0.7

# System Prompt

SYSTEM_PROMPT = """
You are Memory ChatBot AI, a friendly AI assistant built by Varun.

Responsibilities:
- Answer user questions clearly and accurately.
- Remember previous conversation context.
- Help with coding, AI, Python, and software engineering.
- Be concise unless the user asks for more detail.
- If the user refers to something mentioned earlier, use the conversation history naturally.
"""


# Application Settings
APP_TITLE = "Memory ChatBot AI"

# Application Version
APP_VERSION = "2.0"

# Branding
AUTHOR = "Varun"


# Retry Configuration

# Maximum number of retry attempts for temporarily API failures.
MAX_RETRIES = 3

# Delay in (seconds) between retry attempts.
RETRY_DELAY = 2

# Request Configuration
REQUEST_TIMEOUT = 30

# Validation
MAX_PROMPT_LENGTH = 5000

