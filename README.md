# 🎓 StrataAI

**AI-Powered Study Assistant** — Upload PDFs, chat with your documents, generate quizzes, get explanations, and track your learning progress.

---

## 🚀 Features (Roadmap)

- [ ] 📄 PDF Upload & Text Extraction
- [ ] 🔍 Semantic Search with Embeddings
- [ ] 💬 Chat with PDFs (RAG)
- [ ] 📝 AI-Generated Explanations
- [ ] ❓ Quiz Generation (MCQ + Short Answer)
- [ ] ✅ Answer Evaluation & Feedback
- [ ] 📅 Personalized Study Plans
- [ ] 📊 Progress Tracking & Analytics
- [ ] 🤖 Agentic Workflows (LangGraph)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Python |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| LLMs | Google Gemini, Groq |
| Database | SQLite |
| Agent Framework | LangGraph |
| Deployment | Streamlit Cloud |

---

## 📦 Setup

### Prerequisites
- Python 3.10+

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/StrataAI.git
cd StrataAI

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the app
streamlit run app.py
```

---

## 📁 Project Structure

```
StrataAI/
├── app.py                  # Streamlit entry point
├── config/
│   └── settings.py         # Centralized configuration
├── src/
│   ├── pdf/                # PDF extraction & chunking
│   ├── embeddings/         # Embedding pipeline
│   ├── rag/                # RAG chat pipeline
│   ├── explanations/       # Explanation engine
│   ├── quiz/               # Quiz generation
│   ├── evaluation/         # Answer evaluation
│   ├── study_plan/         # Study plan generator
│   ├── progress/           # Progress tracking
│   └── agents/             # LangGraph agents
├── pages/                  # Streamlit multi-page UI
├── data/                   # Runtime data
├── tests/                  # Test suite
└── utils/                  # Shared utilities
```

---

## 📄 License

This project is for educational purposes.

---

*Built with ❤️ as a learning project to master AI engineering.*
