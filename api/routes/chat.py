from fastapi import APIRouter
from api.models.schemas import ChatRequest, ChatResponse
from api.agents.tutor_agent import tutor_agent

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    print(f"Routing message to TutorAgent: {request.message}")
    
    # Generate response from OpenAI
    ai_response = tutor_agent.generate_response(
        user_message=request.message,
        history=request.history
    )
    
    return ChatResponse(
        response=ai_response,
        sources=[]
    )
