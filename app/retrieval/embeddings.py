# app/retrieval/embeddings.py
import os
from typing import List

OPENAI_API_KEY = ""

def openai_embeddings(texts: List[str]):
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        resp = openai.Embedding.create(model="text-embedding-3-small", input=texts)
        return [r["embedding"] for r in resp["data"]]
    except Exception:
        return None

# fallback using sentence-transformers
def local_embeddings(texts: List[str]):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast
    return model.encode(texts, show_progress_bar=False).tolist()

def get_embeddings(texts: List[str]):
    emb = openai_embeddings(texts)
    if emb is not None:
        return emb
    return local_embeddings(texts)
