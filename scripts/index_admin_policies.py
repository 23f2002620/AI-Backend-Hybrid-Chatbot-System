from app.retrieval.store_and_query import store_document
from app.retrieval.embeddings import get_embeddings
from app.retrieval.vector_store import VEC_BACKEND

POLICIES = [
    "Harassment cases must be reviewed within 2 hours.",
    "Explicit sexual content requires immediate ban.",
    "Impersonation leads to permanent suspension.",
    "Threats or violence require law enforcement escalation.",
    "Repeat offenders should be permanently banned."
]

def store_document(owner_type, owner_id, text, meta):
    emb = get_embeddings([text])[0]

    if VEC_BACKEND == "pgvector":
        from app.retrieval.vector_store import store_embedding_pg
        store_embedding_pg(owner_type, owner_id, emb, text, meta)
    else:
        from app.retrieval.vector_store import store_embedding_faiss
        store_embedding_faiss(owner_type, owner_id, emb, text, meta)


for p in POLICIES:
    store_document(
        owner_type="policy",
        owner_id=None,
        text=p,
        meta={"source": "admin_policy"}
    )

print("Admin policies indexed")
