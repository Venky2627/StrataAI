from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str) -> list[str]:
    """
    Splits a large string of text into smaller, overlapping chunks.
    
    Args:
        text (str): The full text extracted from the PDF.
        
    Returns:
        list[str]: A list of text chunks.
    """
    # Create the text splitter instance using our config settings
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    
    # Perform the split
    chunks = text_splitter.split_text(text)
    
    return chunks
