import streamlit as st
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

# We use @st.cache_resource so Streamlit only loads the massive AI model into memory ONCE.
# Without this, Streamlit would reload the 100MB model every time you click a button!
@st.cache_resource
def get_embedding_model():
    """Loads and caches the SentenceTransformer model."""
    # This will download the model from HuggingFace the very first time it runs
    return SentenceTransformer(EMBEDDING_MODEL)

def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Converts a list of text chunks into a list of mathematical vectors.
    
    Args:
        chunks (list[str]): The text chunks to embed.
        
    Returns:
        list[list[float]]: A list where each item is a 384-dimensional vector.
    """
    model = get_embedding_model()
    
    # model.encode() does the heavy lifting.
    # We convert it to a standard Python list so it's easy to store in databases later.
    embeddings = model.encode(chunks).tolist()
    
    return embeddings
