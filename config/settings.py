# ============================================================================
# STRATAAI - CONFIGURATION SETTINGS
# ============================================================================
# WHY THIS FILE EXISTS:
# Hardcoding values like model names, file paths, and chunk sizes throughout
# your codebase is a maintenance nightmare. If you want to switch from
# "gemini-1.5-flash" to "gemini-2.0-flash", you'd have to find and update
# every occurrence across dozens of files.
#
# By centralizing ALL configurable values here, you change ONE file
# and the entire application updates. This is called the
# "Single Source of Truth" principle.
#
# ARCHITECTURE DECISION:
# We use simple Python constants instead of a config library (like pydantic-settings)
# because at this stage, simplicity wins. We'll upgrade if needed later.
# ============================================================================

import os
from pathlib import Path


# --- Project Paths ---
# Path.resolve() converts relative paths to absolute paths.
# This ensures our paths work correctly regardless of WHERE you run the app from.
# Without this, "data/uploads" might resolve differently depending on your terminal's
# current directory, causing "file not found" errors.
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Go up from config/ to StrataAI/
DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
CHROMA_DIR = DATA_DIR / "chroma_db"

# --- Streamlit Page Config ---
# These values are used in app.py to configure the Streamlit page.
# Centralizing them here means the app's branding can be updated in one place.
APP_TITLE = "StrataAI"
APP_ICON = "🎓"
APP_DESCRIPTION = "AI-Powered Study Assistant"

# --- LLM Settings (Week 4+) ---
# We define these now so the structure is ready when we integrate LLMs.
# Empty strings are intentional — the real values come from .env at runtime.
GEMINI_MODEL = "gemini-2.0-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"

# --- Embedding Settings (Week 3) ---
# all-MiniLM-L6-v2 is a popular sentence transformer model.
# "MiniLM" = smaller, faster version of a language model
# "L6" = 6 transformer layers (good balance of speed vs quality)
# "v2" = second version with improved training
# It converts text into 384-dimensional vectors for similarity search.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# --- Chunking Settings (Week 2) ---
# When we split PDFs into chunks, these control the size.
# CHUNK_SIZE: Maximum characters per chunk. 1000 chars ≈ 150-200 words.
#   Too small → loses context. Too large → dilutes relevance in search.
# CHUNK_OVERLAP: Characters shared between consecutive chunks.
#   This prevents important sentences from being split across chunks.
#   If a key sentence sits at position 990-1010, without overlap it would be
#   split between chunk 1 and chunk 2. Overlap ensures it appears fully in chunk 2.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# --- ChromaDB Settings (Week 3) ---
# The name of our vector collection. Think of it like a database table name.
CHROMA_COLLECTION_NAME = "strata_documents"
