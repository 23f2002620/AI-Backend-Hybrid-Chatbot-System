def detect_intent(text):
    t = text.lower()
    if "report" in t:
        return "report"
    if "suggest" in t:
        return "coach"
    return "chat"
