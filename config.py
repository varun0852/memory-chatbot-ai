"""
Application Configuration

This module loads environment variables and stores
all application-wide configuration in one place.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini Model
MODEL_NAME = "gemini-2.5-flash"

# Application Settings
APP_TITLE = "Memory ChatBot"

# Branding
AUTHOR = "Varun"