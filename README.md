# StrataAI

StrataAI is an enterprise-grade, AI-powered study assistant and document comprehension engine. Engineered with an advanced Retrieval-Augmented Generation (RAG) architecture and Agentic workflows, it enables deep analysis, dynamic querying, and automated assessment generation from complex textual data.

---

## Core Capabilities

- **Intelligent Ingestion:** High-fidelity PDF parsing and automated chunking with structural preservation.
- **Semantic Retrieval:** Vectorized knowledge search utilizing `sentence-transformers` (`all-MiniLM-L6-v2`) and ChromaDB.
- **Generative Synthesis:** Contextually aware document querying, dynamic quiz generation, and adaptive study planning powered by Gemini and Groq LLMs.
- **Agentic Evaluation:** Autonomous assessment of user comprehension using LangGraph state-machines.
- **State Management:** Persistent progress tracking via SQLite.

---

## System Architecture

The application strictly adheres to the Separation of Concerns principle, isolating presentation, configuration, and business logic.

```text
StrataAI/
├── .venv/                  # Isolated Python environment
├── config/                 # Centralized configuration variables
├── data/                   # Local storage (Uploads, ChromaDB, SQLite)
├── pages/                  # Streamlit multi-page interface routing
├── src/                    # Core business logic
│   ├── agents/             # LangGraph workflows
│   ├── embeddings/         # Vectorization services
│   ├── evaluation/         # Quiz grading engines
│   ├── explanations/       # Generative simplification logic
│   ├── pdf/                # Document extraction and parsing
│   ├── progress/           # SQLite database operations
│   ├── quiz/               # Assessment generation
│   ├── rag/                # Retrieval and synthesis orchestration
│   └── study_plan/         # Automated curriculum generation
├── tests/                  # Unit and integration tests
├── utils/                  # Shared helper functions
├── .env.example            # Environment variable template
├── .gitignore              # Version control exclusion rules
├── app.py                  # Application entry point and dashboard
└── requirements.txt        # Frozen dependency manifests
```

---

## Development Roadmap

The development lifecycle is structured across 12 distinct implementation weeks.

- **Phase 1: Foundation (Weeks 1-2)**
  Environment setup, architectural routing, and document ingestion (PyMuPDF).
- **Phase 2: Semantic Memory (Weeks 3-4)**
  Vector database integration, embedding models, and initial LLM synthesis.
- **Phase 3: Core Features (Weeks 5-7)**
  Explanation generation, assessment creation, and context-aware grading.
- **Phase 4: Agentic Systems (Weeks 8-10)**
  LangGraph integration for autonomous study planning and user progress tracking.
- **Phase 5: Deployment (Weeks 11-12)**
  System optimization, refactoring, and cloud deployment via Streamlit Community Cloud.

---

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Venky2627/StrataAI.git
   cd StrataAI
   ```

2. **Initialize environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Unix:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Application:**
   ```bash
   streamlit run app.py
   ```

---

*Developed by Venkatesh (Venky2627)*
