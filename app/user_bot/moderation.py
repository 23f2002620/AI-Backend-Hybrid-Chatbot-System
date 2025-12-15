BLOCKED = ["child", "rape", "kill"]

def is_blocked(text):
    return any(word in text.lower() for word in BLOCKED)
