import json
from langchain_core.prompts import PromptTemplate
from src.llm.gemini import get_llm
from src.rag.vectorstore import get_or_create_collection

QUIZ_PROMPT_MCQ = """
You are an expert educational assessment creator.
Your task is to generate a Multiple Choice Quiz based ONLY on the provided context chunks.

Context chunks:
{context}

Generate exactly {num_questions} multiple choice questions.
You MUST output your response as a valid JSON array of objects, with NO markdown formatting, NO backticks, and NO extra text before or after the JSON.
The JSON array must exactly follow this schema:
[
  {{
    "type": "mcq",
    "question": "The text of the question?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option B",
    "explanation": "Explanation of why Option B is correct based on the context."
  }}
]

Make sure "correct_answer" is an exact string match for one of the items in the "options" array.
"""

QUIZ_PROMPT_SHORT = """
You are an expert educational assessment creator.
Your task is to generate a Short Answer Quiz based ONLY on the provided context chunks.

Context chunks:
{context}

Generate exactly {num_questions} short-answer questions that require a 1-3 sentence response.
You MUST output your response as a valid JSON array of objects, with NO markdown formatting, NO backticks, and NO extra text before or after the JSON.
The JSON array must exactly follow this schema:
[
  {{
    "type": "short_answer",
    "question": "The text of the short answer question?"
  }}
]
"""

def generate_quiz(active_documents: list[str] = None, num_questions: int = 5, quiz_type: str = "mcq") -> list[dict]:
    """
    Fetches context from active documents and asks the LLM to generate a JSON quiz.
    Returns a list of dictionary question objects.
    """
    chunks = []
    if active_documents:
        collection = get_or_create_collection()
        if len(active_documents) == 1:
            where_filter = {"source": active_documents[0]}
        else:
            where_filter = {"source": {"$in": active_documents}}
            
        # Get up to 10 chunks to base the quiz on
        results = collection.get(where=where_filter, limit=10)
        if results['documents']:
            chunks = results['documents']
    
    context_text = "\n\n---\n\n".join(chunks) if chunks else "General knowledge context."
    
    prompt_str = QUIZ_PROMPT_SHORT if quiz_type == "short_answer" else QUIZ_PROMPT_MCQ
    prompt_template = PromptTemplate.from_template(prompt_str)
    formatted_prompt = prompt_template.format(context=context_text, num_questions=num_questions)
    
    llm = get_llm()
    # To force JSON, some LLMs have specific arguments, but a strict prompt usually works.
    response = llm.invoke(formatted_prompt)
    
    # Try to parse the output as JSON
    raw_text = response.content.strip()
    # Clean up potential markdown formatting
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    raw_text = raw_text.strip()
    
    try:
        quiz_data = json.loads(raw_text)
        return quiz_data
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM JSON: {e}")
        print(f"Raw Output: {raw_text}")
        return []
