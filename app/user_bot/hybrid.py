from app.user_bot.moderation import is_blocked
from app.user_bot.intent import detect_intent
from app.user_bot.retrieval import retrieve
from app.llm.llm_router import generate_llm_response

def user_bot(message):
    # RULE-BASED SAFETY
    if is_blocked(message):
        return {"reply": "This message violates safety rules."}

    intent = detect_intent(message)

    # RETRIEVAL
    retrieved = retrieve(message)
    if retrieved:
        return {"reply": retrieved, "intent": intent}

    # LLM (WITH FAILOVER)
    response = generate_llm_response(
        f"You are a dating assistant. Be friendly.\nUser: {message}"
    )

    return {"reply": response, "intent": intent}
