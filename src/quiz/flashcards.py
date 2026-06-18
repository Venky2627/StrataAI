import json
import time
from langchain_core.prompts import PromptTemplate
from src.llm.gemini import get_llm

FLASHCARD_PROMPT = """
You are an expert educational content creator.
Your task is to analyze the provided document text and generate a deck of highly concise, bite-sized flashcards.

Document Text:
{text}

Number of Flashcards requested: {num_cards}

Rules:
1. Each flashcard MUST have a "front" (the question, concept, or term) and a "back" (the extremely concise answer or definition).
2. The front should be short (1-2 sentences max).
3. The back should be short and punchy (1-3 sentences max).
4. Output your response as a valid JSON array of objects, with NO markdown formatting, NO backticks, and NO extra text.
5. The JSON array must exactly follow this schema:
[
  {{
    "front": "What is the primary function of mitochondria?",
    "back": "To generate most of the chemical energy needed to power the cell's biochemical reactions."
  }},
  {{
    "front": "Define Opportunity Cost.",
    "back": "The potential benefit that is lost when you choose one alternative over another."
  }}
]
"""

def generate_flashcards(document_text: str, num_cards: int = 15) -> list[dict]:
    """
    Generates a list of flashcard dictionaries using the LLM based on document content.
    Includes rate limit handling and text truncation to save token quota.
    """
    # Truncate text to 20,000 characters to prevent free-tier TPM limit exhaustion
    truncated_text = document_text[:20000] if document_text else "General knowledge domain."
    
    prompt_template = PromptTemplate.from_template(FLASHCARD_PROMPT)
    formatted_prompt = prompt_template.format(
        text=truncated_text,
        num_cards=num_cards
    )
    
    llm = get_llm()
    
    # Exponential Backoff for Quota Limits
    max_retries = 3
    base_delay = 5
    
    for attempt in range(max_retries):
        try:
            response = llm.invoke(formatted_prompt)
            break
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < max_retries - 1:
                    wait_time = base_delay * (2 ** attempt)
                    print(f"Rate limit hit in flashcards. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception("AI API quota exceeded. Please try again in a minute.")
            else:
                raise e
    
    # Parse JSON
    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        deck = json.loads(content.strip())
        return deck
    except Exception as e:
        raise ValueError(f"Failed to parse flashcard JSON: {str(e)}\nRaw Output: {response.content}")
