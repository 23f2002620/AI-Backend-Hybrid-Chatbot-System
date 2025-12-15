"""
uvicorn app.main:app --reload
python -m scripts.index_admin_policies
python -m scripts.index_faq_and_recent

Invoke-RestMethod `                      
   -Uri "http://127.0.0.1:8000/user/chat" ` 
   -Method POST `
   -Headers @{ "Content-Type" = "application/json" } `
   -Body (Get-Content tests/user.json -Raw) 


Invoke-RestMethod `
   -Uri "http://127.0.0.1:8000/admin/chat" `
   -Method POST `
   -Headers @{ "Content-Type"="application/json" } `
   -Body '{"query":"harassment","user":{"reports":4,"trust":30}}' |
ConvertTo-Json -Depth 6
"""




from fastapi import FastAPI
from app.database import init_db
from app.user_bot.router import router as user_router
from app.admin_bot.router import router as admin_router

app = FastAPI(title="Dating App AI Backend")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(user_router)
app.include_router(admin_router)
