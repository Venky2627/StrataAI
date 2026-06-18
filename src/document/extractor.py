import fitz  # PyMuPDF
import io
import re
import docx
import base64
from src.llm.gemini import get_llm
from langchain_core.messages import HumanMessage

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """
    Master router that checks the file extension and sends the bytes 
    to the correct extraction engine.
    """
    ext = filename.split(".")[-1].lower()
    
    if ext == "pdf":
        text = extract_text_from_pdf(file_bytes)
    elif ext == "docx":
        text = extract_text_from_docx(file_bytes)
    elif ext in ["txt", "md", "csv"]:
        text = extract_text_from_raw(file_bytes)
    elif ext in ["png", "jpg", "jpeg"]:
        text = extract_text_from_image(file_bytes, ext)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
        
    return clean_extracted_text(text)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        pdf_document = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
    except Exception as e:
        raise ValueError(f"Failed to read PDF file. Error: {e}")

    extracted_text = []
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text("text")
        if text:
            extracted_text.append(text)

    return "\n".join(extracted_text)

def extract_text_from_docx(docx_bytes: bytes) -> str:
    try:
        doc = docx.Document(io.BytesIO(docx_bytes))
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Failed to read DOCX file. Error: {e}")

def extract_text_from_raw(raw_bytes: bytes) -> str:
    try:
        return raw_bytes.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to decode text file as UTF-8. Error: {e}")

def extract_text_from_image(image_bytes: bytes, mime_ext: str) -> str:
    """
    Uses Gemini 2.5 Flash's massive multimodal capability as an OCR engine!
    """
    mime_type = f"image/{mime_ext}" if mime_ext != "jpg" else "image/jpeg"
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    llm = get_llm()
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": "You are a perfect OCR engine. Extract and transcribe absolutely ALL text visible in this image accurately. Do not summarize. Just return the text."},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
            }
        ]
    )
    
    response = llm.invoke([message])
    return response.content

def clean_extracted_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
