import json
from langchain_core.prompts import PromptTemplate
from src.llm.gemini import get_llm

PLANNER_PROMPT = """
You are an expert academic tutor and productivity coach.
Your task is to analyze the provided document text and create a highly structured, day-by-day study schedule.

User's Constraints:
- Total Days: {days}
- Hours per Day: {hours}
- Goal: {goal}

Document Text:
{text}

You MUST output your response as a valid JSON array of objects, with NO markdown formatting, NO backticks, and NO extra text.
The JSON array must exactly follow this schema, where each object represents one day:
[
  {{
    "day": 1,
    "title": "Introduction to the Core Concepts",
    "topics": ["Topic A", "Topic B"],
    "time_allocation": "2 hours",
    "action_items": ["Read chapter 1", "Summarize key terms"],
    "tips": "Focus on understanding the big picture before diving into formulas."
  }},
  {{
    "day": 2,
    "title": "...",
    "topics": ["..."],
    "time_allocation": "...",
    "action_items": ["..."],
    "tips": "..."
  }}
]

Make sure the schedule logically builds up knowledge from the document text and strictly respects the user's total days and hours per day.
"""

def generate_study_plan(document_text: str, days: int, hours: int, goal: str) -> list[dict]:
    """
    Generates a structured JSON study schedule using the LLM based on document content and constraints.
    """
    import time
    
    # We heavily truncate the text to 15,000 characters to avoid hitting Token Per Minute (TPM) limits on the free tier.
    # 15k characters is usually enough to capture the Table of Contents and introductory concepts.
    truncated_text = document_text[:15000] if document_text else "General knowledge domain."
    
    prompt_template = PromptTemplate.from_template(PLANNER_PROMPT)
    formatted_prompt = prompt_template.format(
        text=truncated_text,
        days=days,
        hours=hours,
        goal=goal
    )
    
    llm = get_llm()
    
    # Simple Exponential Backoff to handle 429 Quota/Rate Limit Exhaustion
    max_retries = 3
    base_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            response = llm.invoke(formatted_prompt)
            break # Success, exit retry loop
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < max_retries - 1:
                    wait_time = base_delay * (2 ** attempt)
                    print(f"Rate limit hit. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception("AI API quota exceeded and max retries reached. Please try again in a minute.")
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
            
        schedule = json.loads(content.strip())
        return schedule
    except Exception as e:
        raise ValueError(f"Failed to parse study plan JSON: {str(e)}\nRaw Output: {response.content}")
