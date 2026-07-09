# 🤖 Memory ChatBot AI

A production-ready conversational AI assistant built with **Streamlit**, **Groq LLM**, and modern software engineering practices. Memory ChatBot AI features persistent conversation history, PDF document chat, conversation analytics, import/export capabilities, and a modular architecture designed for maintainability and scalability.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-LLM-black?style=for-the-badge)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🚀 Live Demo

### 🌐 Try the application

**https://memory-chatbot-ai-uw69hmnown9nzxj7kxouft.streamlit.app/**

---

## 🎬 Demo

<p align="center">
<img src="assets/demo/memory-chatbot-demo.gif" width="900">
</p>

---

# 📸 Screenshots

## 🏠 Welcome Screen

![](assets/screenshots/welcome.png)

---

## 💬 AI Conversation

![](assets/screenshots/chat.png)

---

## 📄 Chat with PDF Documents

![](assets/screenshots/document-chat.png)

---

## 📚 Conversation History

![](assets/screenshots/conversation-history.png)

---

## 📊 Analytics Dashboard

![](assets/screenshots/analytics.png)

---

## 📤 Export Conversations

![](assets/screenshots/export.png)

---

## 📥 Import Conversations

![](assets/screenshots/import.png)

---

# ✨ Features

## 💬 Conversation Management

- Multi-turn AI conversations
- Persistent conversation history
- Search previous conversations
- Delete conversations
- Automatic session management

---

## 📄 Document Chat

- Upload PDF documents
- Ask questions about uploaded documents
- Extract document text automatically
- Remove documents anytime

---

## 📤 Import & Export

Supports multiple export formats:

- TXT
- Markdown
- PDF
- Memory Chat Package (.chat)

Import previously exported conversations with one click.

---

## 📊 Analytics

Real-time conversation insights:

- Total conversations
- Total messages
- User / Assistant message counts
- Average messages per conversation
- Session duration
- Character count
- Word count
- Export statistics

---

## 🤖 AI Experience

- Groq LLM integration
- Streaming responses
- Multiple model selection
- Secure API key handling
- Context-aware conversations

---

## 🛠 Developer Experience

- Modular architecture
- SQLite persistence
- Automated testing
- Ruff linting
- Black formatting
- Comprehensive documentation
- Changelog & Release Notes

---

# 🏗 Architecture

```
                         User
                           │
                           ▼
                 Streamlit Application
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Components            Backend             Database
        │                  │                  │
        ▼                  ▼                  ▼
 Document Chat      ChatBot Engine      SQLite Storage
 Export System      Groq Client         Conversation DB
 Analytics          Validation          Session History
```

---

# 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | Streamlit |
| LLM | Groq |
| Language | Python 3.11 |
| Database | SQLite |
| PDF Processing | PyPDF2 |
| PDF Export | ReportLab |
| Testing | Pytest |
| Formatting | Black |
| Linting | Ruff |

---

# 📁 Project Structure

```text
MemoryChatbot/
├── assets/
│   ├── demo/
│   └── screenshots/
├── backend/
├── components/
├── database/
├── docs/
├── models/
├── tests/
├── utils/
├── .streamlit/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
└── LICENSE
```

---

# 🔧 Installation

Clone the repository

```bash
git clone https://github.com/varun0852/memory-chatbot-ai.git

cd memory-chatbot-ai
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙ Configuration

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# 🚀 Run the Application

```bash
streamlit run app.py
```

---

# 🧪 Testing

Run all tests

```bash
python -m pytest
```

Run Ruff

```bash
ruff check .
```

Run Black

```bash
black .
```

Current Status

- ✅ 14 Automated Tests
- ✅ Ruff Checks Passed
- ✅ Black Formatting Applied

---

# ☁ Deployment

The application is deployed on **Streamlit Community Cloud**.

Live URL

https://memory-chatbot-ai-uw69hmnown9nzxj7kxouft.streamlit.app/

---

# 🗺 Roadmap

### Version 2.x

- [x] Conversation History
- [x] Conversation Search
- [x] Analytics Dashboard
- [x] PDF Document Chat
- [x] Conversation Import/Export
- [x] Modular Architecture
- [x] Automated Tests

### Future Improvements

- [ ] Multi-provider LLM Support
- [ ] Image Understanding
- [ ] Voice Chat
- [ ] RAG Knowledge Base
- [ ] Docker Support
- [ ] CI/CD Pipeline
- [ ] Authentication
- [ ] Cloud Database Support

---

# 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---

## 👤 Author

**Varun** — AI/ML Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/varun-a87781274/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/varun0852)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:diwakarvarun752@gmail.com)
