import chromadb
from config.settings import CHROMA_DIR, CHROMA_COLLECTION_NAME

def get_chroma_client():
    """Initializes and returns a persistent ChromaDB client."""
    # Convert Path object to string because ChromaDB expects a string path
    return chromadb.PersistentClient(path=str(CHROMA_DIR))

def get_or_create_collection():
    """Gets an existing collection or creates a new one."""
    client = get_chroma_client()
    return client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

def store_documents(filename: str, chunks: list[str], embeddings: list[list[float]]):
    """
    Stores chunks and their embeddings into ChromaDB permanently.
    """
    collection = get_or_create_collection()
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename} for _ in range(len(chunks))]
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

def search_documents(query_embedding: list[float], n_results: int = 3, where_filter: dict = None):
    """
    Searches the database for chunks that mathematically match the query vector.
    
    Args:
        query_embedding (list[float]): The mathematical vector of the user's question.
        n_results (int): How many chunks to return (default 3).
        where_filter (dict): Optional metadata filter for ChromaDB.
        
    Returns:
        dict: The raw ChromaDB results dictionary.
    """
    collection = get_or_create_collection()
    
    kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": n_results
    }
    if where_filter:
        kwargs["where"] = where_filter
        
    results = collection.query(**kwargs)
    
    return results
