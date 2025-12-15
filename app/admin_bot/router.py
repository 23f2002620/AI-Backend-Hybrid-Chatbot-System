from fastapi import APIRouter
from pydantic import BaseModel
from app.admin_bot.admin import admin_bot

router = APIRouter()

class AdminInput(BaseModel):
    query: str
    user: dict

@router.post("/admin/chat")
def chat(inp: AdminInput):
    return admin_bot(inp.query, inp.user)
