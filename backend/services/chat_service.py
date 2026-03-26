from ml.emotion_model import detect_emotion
from services.llm_service import generate_llm_response
from db.chat_repository import save_chat

def process_chat(message: str):
    # Step 1: Detect emotion
    emotion = detect_emotion(message)

    # Step 2: Generate AI response (LLM 🔥)
    response = generate_llm_response(message, emotion)

    # Step 3: Save chat
    save_chat(message, emotion, response)

    return {
        "emotion": emotion,
        "response": response
    }