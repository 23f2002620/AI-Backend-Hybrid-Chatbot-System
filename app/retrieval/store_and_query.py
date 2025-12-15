# app/retrieval/store_and_query.py

from app.retrieval.embeddings import get_embeddings
from app.retrieval.vector_store import VEC_BACKEND

def store_document(owner_type, owner_id, text, meta):
    emb = get_embeddings([text])[0]

    if VEC_BACKEND == "pgvector":
        from app.retrieval.vector_store import store_embedding_pg
        store_embedding_pg(owner_type, owner_id, emb, text, meta)
    else:
        from app.retrieval.vector_store import store_embedding_faiss
        store_embedding_faiss(owner_type, owner_id, emb, text, meta)


def query_similar(text, top_k=5):
    emb = get_embeddings([text])[0]

    if VEC_BACKEND == "pgvector":
        from app.retrieval.vector_store import pgvector_query
        return pgvector_query(emb, top_k)
    else:
        from app.retrieval.vector_store import query_embeddings_faiss
        return query_embeddings_faiss(emb, top_k)
