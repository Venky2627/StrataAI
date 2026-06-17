import os
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_MODEL

def get_llm():
    """
    Initializes and returns the Gemini Large Language Model.
    Requires GEMINI_API_KEY to be set in the .env file.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "paste_your_api_key_here":
        raise ValueError("CRITICAL ERROR: GEMINI_API_KEY is missing or invalid in your .env file!")
        
    # We use temperature=0.3. 
    # 0.0 = completely robotic and predictable. 
    # 1.0 = highly creative and hallucination-prone.
    # 0.3 is perfect for RAG: factual but conversational.
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0.3,
        google_api_key=api_key
    )
