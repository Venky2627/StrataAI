import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "StrataAI OS"
    GEMINI_API_KEY: str = ""
    
    # Vector DB path
    CHROMA_PERSIST_DIR: str = "./chroma_db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
