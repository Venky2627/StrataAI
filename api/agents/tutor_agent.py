import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from api.core.config import settings
from api.models.schemas import ChatMessage

class TutorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
            google_api_key=settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
        )
        
        self.system_prompt = """You are StrataAI, a deeply technical, venture-backed AI Learning Operating System.
You speak clearly, concisely, and intelligently. 
You act as a world-class tutor and second brain for the user.
Your interface is minimalist and cinematic.
Do not use emojis unless absolutely necessary.
Format responses in clean Markdown.
If the user asks for explanations, break them down clearly but do not patronize them."""

    def generate_response(self, user_message: str, history: list[ChatMessage]) -> str:
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Append history
        for msg in history:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))
                
        # Append latest user message
        messages.append(HumanMessage(content=user_message))
        
        response = self.llm.invoke(messages)
        return response.content

# Singleton instance
tutor_agent = TutorAgent()
