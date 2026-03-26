from db.chat_repository import save_chat, get_recent_chats, get_emotion_summary
from ml.emotion_model import detect_emotion
from services.llm_service import generate_llm_response


def process_chat(message: str, user_id="default_user"):

    # 🧠 Emotion detection
    emotion = detect_emotion(message)

    # 🧠 MEMORY: get last chats
    past_chats = get_recent_chats(user_id)

    context = ""
    for chat in reversed(past_chats):
        context += f"User: {chat.message}\nAssistant: {chat.response}\n"

    # 📊 PERSONALIZATION: emotion trend
    emotion_summary = get_emotion_summary(user_id)

    trend = ", ".join([f"{k}:{v}" for k, v in emotion_summary.items()])

    # 🧠 FINAL PROMPT
    prompt = f"""
You are a mental health assistant helping students.

User emotion: {emotion}
Emotion trend: {trend}

Conversation history:
{context}

User: {message}

Give a supportive, empathetic, and helpful response.
"""

    # 🤖 LLM call
    response = generate_llm_response(prompt, emotion)

    # 💾 Save chat
    save_chat(user_id, message, emotion, response)

    return {
        "emotion": emotion,
        "response": response
    }