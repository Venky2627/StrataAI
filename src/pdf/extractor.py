import fitz  # PyMuPDF is imported as 'fitz' (its original name was default_api:Fitz)
import io
import re


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts and cleans text from a PDF file provided as raw bytes.
    
    Args:
        pdf_bytes (bytes): The raw binary content of the PDF file.
        
    Returns:
        str: The extracted, cleaned text from all pages.
    """
    # 1. Load the raw bytes into a PyMuPDF Document object.
    # We use io.BytesIO to treat the raw bytes like a physical file.
    # "pdf" tells PyMuPDF what format to expect.
    try:
        pdf_document = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
    except Exception as e:
        raise ValueError(f"Failed to read PDF file. It might be corrupted. Error: {e}")

    extracted_text = []

    # 2. Iterate through every page in the document
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Extract text from the current page
        text = page.get_text("text")
        
        if text:
            extracted_text.append(text)

    # 3. Join all pages into one massive string, separated by newlines
    full_text = "\n".join(extracted_text)

    # 4. Clean the text
    cleaned_text = clean_extracted_text(full_text)

    return cleaned_text


def clean_extracted_text(text: str) -> str:
    """
    Cleans raw PDF text to remove noise that confuses LLMs.
    """
    if not text:
        return ""

    # Replace multiple spaces with a single space
    # Example: "The   cell is  small" -> "The cell is small"
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Replace 3 or more consecutive newlines with exactly 2 newlines
    # This preserves paragraph breaks but removes massive vertical gaps
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    
    return text
