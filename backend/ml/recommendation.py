def generate_recommendation(emotion: str) -> str:
    if emotion == "stress":
        return "You seem stressed. Try deep breathing or take a short break."
    
    elif emotion == "sad":
        return "It's okay to feel sad. Talk to someone you trust or write your thoughts."

    elif emotion == "anxiety":
        return "Try grounding techniques or meditation to reduce anxiety."

    elif emotion == "happy":
        return "That's great! Keep doing what makes you happy."

    return "I'm here for you. Tell me more about how you're feeling."