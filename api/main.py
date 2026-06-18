from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.routes import chat

app = FastAPI(
    title="StrataAI OS Core",
    description="The intelligent backend powering StrataAI.",
    version="2.0.0",
)

# CORS for local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "online", "system": "StrataAI OS"}

# Placeholder endpoints for Phase 1 migration
@app.post("/api/documents/upload")
async def upload_document():
    # TODO: Integrate src.ingestion
    return {"status": "success", "message": "Document ingested"}

app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/api/progress/cognitive-profile")
async def cognitive_profile():
    # TODO: Integrate src.db
    return {
        "learningVelocity": 85,
        "retentionRate": 92,
        "masteryGrowth": 15,
    }
