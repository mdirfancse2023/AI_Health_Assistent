# Simple version (you can upgrade later to BERT)

def detect_emotion(text: str) -> str:
    text = text.lower()

    if "stress" in text or "pressure" in text:
        return "stress"
    elif "sad" in text or "depressed" in text:
        return "sad"
    elif "happy" in text:
        return "happy"
    elif "anxious" in text:
        return "anxiety"
    
    return "neutral"