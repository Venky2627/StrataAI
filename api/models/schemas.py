from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    document_ids: Optional[List[str]] = []

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []
