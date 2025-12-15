from app.retrieval.store_and_query import query_similar

MIN_SCORE = 0.45  # confidence threshold


def retrieve_policy_or_cases(query: str, top_k: int = 5):
    """
    Semantic retrieval with:
    - confidence threshold
    - duplicate removal
    """

    raw_results = query_similar(query, top_k=top_k)

    seen_texts = set()
    cleaned = []

    for _, score, text in raw_results:
        if score < MIN_SCORE:
            continue

        normalized = text.strip().lower()
        if normalized in seen_texts:
            continue

        seen_texts.add(normalized)

        cleaned.append({
            "score": round(score, 3),
            "text": text
        })

    return cleaned
