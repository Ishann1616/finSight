from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from routers.auth import get_current_user
from agent.agent import run_agent

router=APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user= Depends(get_current_user),
    db: Session= Depends(get_db)
):
    try:
        response = run_agent(current_user.id, request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500 ,detail=str(e))
    