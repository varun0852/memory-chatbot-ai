# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by **Keep a Changelog** and follows **Semantic Versioning**.

---

## [2.0.0] - 2026-07-09

### Added

- Modular component-based Streamlit architecture
- Conversation history with persistent SQLite storage
- Conversation search
- Conversation analytics dashboard
- Current session insights
- PDF document chat
- Portable `.chat` conversation export
- Portable `.chat` conversation import
- Professional PDF conversation export
- Markdown conversation export
- Plain text conversation export
- Multi-stage status updates using `st.status()`
- Configurable AI model selection
- Comprehensive automated test suite

### Changed

- Refactored `app.py` into a lightweight application coordinator
- Extracted reusable Streamlit UI components
- Improved session initialization
- Improved conversation management
- Improved import/export workflow
- Improved error handling
- Added strong type hints throughout the project
- Standardized code formatting with Black
- Added Ruff linting
- Improved project documentation

### Fixed

- Fixed conversation import session ID conflicts
- Fixed conversation export counter updates
- Fixed invalid conversation package validation
- Fixed conversation search behavior
- Fixed Windows compatibility during automated database tests
- Fixed malformed import package handling
- Improved overall application stability