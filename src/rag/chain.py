from langchain_core.prompts import PromptTemplate
from src.llm.gemini import get_llm
from src.rag.vectorstore import search_documents
from src.embeddings.generator import generate_embeddings
from src.explanations.personas import get_persona_prompt

def answer_question(query: str, active_documents: list[str] = None, persona_name: str = "Standard Tutor") -> tuple[str, list[str]]:
    """
    The full RAG pipeline!
    1. If documents exist, embeds the question and searches ChromaDB.
    2. Prompts Gemini with the chunks (if any) + question.
    
    Returns the AI's answer and the source chunks used.
    """
    chunks = []
    
    # 1. Search the database only if there are active documents
    if active_documents:
        query_vector = generate_embeddings([query])[0]
        
        if len(active_documents) == 1:
            where_filter = {"source": active_documents[0]}
        else:
            where_filter = {"source": {"$in": active_documents}}
            
        results = search_documents(query_vector, n_results=3, where_filter=where_filter)
        
        if results['documents'] and results['documents'][0]:
            chunks = results['documents'][0]
    
    # 2. Stitch the chunks together (or pass empty note if no chunks)
    context_text = "\n\n---\n\n".join(chunks) if chunks else "No documents uploaded or nothing relevant found."
    
    # 3. Inject the chunks and the question into our chosen Persona Prompt Template
    rag_prompt = get_persona_prompt(persona_name)
    
    # Hidden system instruction for inline quizzes
    inline_quiz_instruction = """
    
    CRITICAL SYSTEM INSTRUCTION:
    If the user explicitly asks for a quiz, multiple choice question, short answer question, or a test, do NOT reply with normal text. 
    Instead, you MUST reply with a strict JSON array wrapped in [QUIZ_JSON] tags.
    
    You have two types of questions you can generate: "mcq" and "short_answer".
    
    Example for MCQ:
    [QUIZ_JSON]
    [
      {{
        "type": "mcq",
        "question": "...",
        "options": ["...", "...", "...", "..."],
        "correct_answer": "...",
        "explanation": "..."
      }}
    ]
    [/QUIZ_JSON]
    
    Example for Short Answer:
    [QUIZ_JSON]
    [
      {{
        "type": "short_answer",
        "question": "..."
      }}
    ]
    [/QUIZ_JSON]
    """
    
    rag_prompt += inline_quiz_instruction
    prompt_template = PromptTemplate.from_template(rag_prompt)
    formatted_prompt = prompt_template.format(context=context_text, question=query)
    
    # 4. Hand the prompt to Gemini!
    llm = get_llm()
    response = llm.invoke(formatted_prompt)
    
    return response.content, chunks
