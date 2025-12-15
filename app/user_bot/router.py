from fastapi import APIRouter
from pydantic import BaseModel
from app.user_bot.hybrid import user_bot

router = APIRouter()

class UserInput(BaseModel):
    user_id: int
    message: str

@router.post("/user/chat")
def chat(inp: UserInput):
    return user_bot(inp.message)
