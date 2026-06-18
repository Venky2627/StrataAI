import json
import os
from pathlib import Path

# Path to the lightweight JSON database
DATA_DIR = Path(__file__).parent.parent.parent / "data"
PERSONAS_DB_PATH = DATA_DIR / "personas.json"

def get_all_personas() -> list[str]:
    """Returns a list of all available persona names from the database."""
    try:
        with open(PERSONAS_DB_PATH, "r", encoding="utf-8") as f:
            personas = json.load(f)
            return list(personas.keys())
    except Exception as e:
        print(f"Error loading personas database: {e}")
        return ["Standard Tutor"]

def get_persona_prompt(persona_name: str) -> str:
    """Fetches the system prompt for a specific persona. Fallback to Standard Tutor if not found."""
    try:
        with open(PERSONAS_DB_PATH, "r", encoding="utf-8") as f:
            personas = json.load(f)
            return personas.get(persona_name, personas.get("Standard Tutor", "{context}\n{question}"))
    except Exception as e:
        print(f"Error reading persona prompt: {e}")
        return "{context}\n{question}"
