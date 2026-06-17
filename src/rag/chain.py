from langchain_core.prompts import PromptTemplate
from src.llm.gemini import get_llm
from src.rag.vectorstore import search_documents
from src.embeddings.generator import generate_embeddings

# This is the "System Prompt". It sets the absolute rules for the AI.
RAG_PROMPT = """
You are StrataAI, a highly intelligent and helpful expert tutor for college students.
Your goal is to TEACH the student and answer their questions perfectly.

Rules:
1. If the user asks for a definition or explanation of a concept (e.g., "What is probability?"), you MUST provide a clear, easy-to-understand explanation using your own vast knowledge as a tutor.
2. After explaining the concept, you should look at the provided context chunks. If the chunks mention the topic (even if just as a syllabus outline), you can briefly add "In your documents, this is covered under..." to connect it back to their coursework.
3. If the user asks a highly specific question about their document ("What is the grading policy?"), answer strictly from the context chunks.
4. Be clear, concise, and conversational. Don't be robotic.

Context chunks from the user's uploaded PDFs:
{context}

User's Question:
{question}

Helpful Tutor Answer:"""

def answer_question(query: str) -> tuple[str, list[str]]:
    """
    The full RAG pipeline!
    1. Embeds the user's question
    2. Searches ChromaDB for relevant chunks
    3. Prompts Gemini with the chunks + question
    
    Returns the AI's answer and the source chunks used.
    """
    # 1. Convert the question to math and search the database
    query_vector = generate_embeddings([query])[0]
    results = search_documents(query_vector, n_results=3)
    
    # Defensive check: if the database is totally empty
    if not results['documents'] or not results['documents'][0]:
        return "You haven't uploaded any documents yet! Please go to the Upload page first.", []
        
    chunks = results['documents'][0]
    
    # 2. Stitch the 3 chunks together into one massive string separated by lines
    context_text = "\n\n---\n\n".join(chunks)
    
    # 3. Inject the chunks and the question into our Prompt Template
    prompt_template = PromptTemplate.from_template(RAG_PROMPT)
    formatted_prompt = prompt_template.format(context=context_text, question=query)
    
    # 4. Hand the massive prompt to Gemini!
    llm = get_llm()
    response = llm.invoke(formatted_prompt)
    
    return response.content, chunks
