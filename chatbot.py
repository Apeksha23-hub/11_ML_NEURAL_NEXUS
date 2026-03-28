from fastapi import APIRouter
from api.schemas import ChatRequest, ChatResponse
from api.llm_service import chat_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    """
    Handle incoming chat queries and context to generate AI responses.
    """
    reply = chat_response(
        query=request.query, 
        context=request.context, 
        history=request.history
    )
    return {"reply": reply}
