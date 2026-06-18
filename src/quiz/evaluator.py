import json
from langchain_core.prompts import PromptTemplate
from src.llm.gemini import get_llm
from src.rag.vectorstore import get_or_create_collection

EVALUATION_PROMPT = """
You are an expert academic grader.
Your task is to evaluate the user's written answer to a specific question, based ONLY on the provided context chunks.

Context chunks:
{context}

Question: {question}
User's Answer: {user_answer}

You MUST output your response as a valid JSON object, with NO markdown formatting, NO backticks, and NO extra text before or after the JSON.
The JSON object must exactly follow this schema:
{{
  "score": <an integer between 0 and 10>,
  "feedback": "Detailed feedback explaining what the user got right, what they missed based on the context, and how to improve."
}}
"""

def evaluate_answer(active_documents: list[str], question: str, user_answer: str) -> dict:
    """
    Evaluates a user's answer against the context of active documents.
    Returns a dict containing 'score' and 'feedback'.
    """
    collection = get_or_create_collection()
    
    chunks = []
    if active_documents:
        if len(active_documents) == 1:
            where_filter = {"source": active_documents[0]}
        else:
            where_filter = {"source": {"$in": active_documents}}
            
        results = collection.query(
            query_texts=[question],
            n_results=5,
            where=where_filter
        )
        chunks = results['documents'][0] if results and results['documents'] else []
        
    context_text = "\n\n---\n\n".join(chunks) if chunks else "No relevant context found in documents. Grade based on general knowledge."
    
    # 2. Build Prompt
    prompt_template = PromptTemplate.from_template(EVALUATION_PROMPT)
    formatted_prompt = prompt_template.format(
        context=context_text,
        question=question,
        user_answer=user_answer
    )
    
    # 3. Call LLM
    llm = get_llm()
    response = llm.invoke(formatted_prompt)
    
    # 4. Parse JSON
    try:
        content = response.content.strip()
        # Clean up any potential markdown backticks just in case the LLM disobeys
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        evaluation = json.loads(content.strip())
        return evaluation
    except Exception as e:
        return {
            "score": 0,
            "feedback": f"Failed to parse evaluation: {str(e)}\nRaw Output: {response.content}"
        }
