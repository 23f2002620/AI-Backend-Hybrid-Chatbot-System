# scripts/index_faq_and_recent.py
from app.retrieval.store_and_query import store_document
from app.database import SessionLocal
from app.models import EmbeddingsMeta, BotMessage

# Index FAQ
FAQ = {
    "boost": "Boost increases profile visibility for 30 minutes.",
    "superlike": "Superlike shows strong interest and notifies the person."
}
for k, v in FAQ.items():
    store_document("faq", None, f"{k} - {v}", {"source":"faq"})

# Index recent bot messages (last N)
sess = SessionLocal()
msgs = sess.query(BotMessage).order_by(BotMessage.created_at.desc()).limit(200).all()
for m in msgs:
    store_document("message", m.id, m.message, {"session_id": m.session_id})
sess.close()
print("Indexing complete")
