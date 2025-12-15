FAQ = {
    "boost": "Boost increases visibility for 30 minutes.",
    "superlike": "Superlike shows strong interest."
}

def retrieve(text):
    for k,v in FAQ.items():
        if k in text.lower():
            return v
    return None
