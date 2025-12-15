# app/retrieval/vector_store.py
import os
from typing import List, Tuple

VEC_BACKEND = os.getenv("VECTOR_BACKEND", "faiss")  # 'pgvector' or 'faiss'
TOP_K = int(os.getenv("VECTOR_TOP_K", "5"))

if VEC_BACKEND == "pgvector":
    # uses Postgres + pgvector extension; assumes embeddings stored in table embeddings_meta with vector column 'embedding'
    from sqlalchemy import text
    from app.database import SessionLocal

    def pgvector_query(query_embedding, top_k=TOP_K) -> List[Tuple[int, float, str]]:
        """
        Returns list of (owner_id, score, text)
        """
        sess = SessionLocal()
        # Use <-> operator for pgvector (cosine for example) - adjust depending on installation
        sql = text("""
            SELECT id, text, 1 - (embedding <#> :vec) as score
            FROM embeddings_meta
            ORDER BY embedding <#> :vec
            LIMIT :k
        """)
        # :vec needs to be an array; psycopg2 adapter handles.
        res = sess.execute(sql, {"vec": query_embedding, "k": top_k}).fetchall()
        sess.close()
        return [(r[0], float(r[2]), r[1]) for r in res]

    def store_embedding_pg(owner_type, owner_id, embedding, text, metadata):
        sess = SessionLocal()
        # embedding must be cast to vector type; use proper SQL or ORM binding
        sql = text("INSERT INTO embeddings_meta(owner_type, owner_id, embedding, text, metadata) VALUES (:ot,:oid,:vec,:text,:meta)")
        sess.execute(sql, {"ot":owner_type,"oid":owner_id,"vec":embedding,"text":text,"meta":metadata})
        sess.commit()
        sess.close()

else:
    # FAISS backend (local)
    import faiss
    import numpy as np
    from pathlib import Path
    import json
    INDEX_PATH = Path("./faiss_index.index")
    METADATA_PATH = Path("./faiss_meta.json")

    # Use an in-memory index (IndexFlatIP or HNSW) - use cosine by normalizing vectors
    dim = 384  # matches sentence-transformers/all-MiniLM-L6-v2
    index = None
    metadata = []  # list of dicts {id, owner_type, owner_id, text, metadata}

    def ensure_index():
        global index, metadata
        if index is None:
            if INDEX_PATH.exists() and METADATA_PATH.exists():
                index = faiss.read_index(str(INDEX_PATH))
                metadata = json.loads(METADATA_PATH.read_text())
            else:
                index = faiss.IndexFlatIP(dim)
                metadata = []

    def faiss_store(owner_type, owner_id, embedding, text, meta):
        ensure_index()
        vec = np.array(embedding, dtype='float32')
        # normalize to unit vectors for cosine similarity with inner product
        faiss.normalize_L2(vec.reshape(1, -1))
        new_id = len(metadata)
        index.add(vec.reshape(1, -1))
        metadata.append({"id": new_id, "owner_type": owner_type, "owner_id": owner_id, "text": text, "metadata": meta})
        INDEX_PATH.write_bytes(faiss.serialize_index(index))
        METADATA_PATH.write_text(json.dumps(metadata))

    def faiss_query(query_embedding, top_k=TOP_K):
        ensure_index()
        import numpy as np
        if index.ntotal == 0:
            return []
        q = np.array(query_embedding, dtype='float32').reshape(1, -1)
        faiss.normalize_L2(q)
        D, I = index.search(q, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0:
                continue
            m = metadata[idx]
            results.append((m["owner_id"], float(dist), m["text"]))
        return results

    # wrapper functions
    def store_embedding_faiss(owner_type, owner_id, embedding, text, metadata_dict):
        faiss_store(owner_type, owner_id, embedding, text, metadata_dict)

    def query_embeddings_faiss(query_embedding, top_k=TOP_K):
        return faiss_query(query_embedding, top_k)
