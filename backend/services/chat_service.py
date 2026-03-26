import re
from db.chat_repository import save_chat, get_recent_chats, get_emotion_summary
from ml.emotion_model import detect_emotion
from ml.rag_model import retrieve_context
from ml.recommendation import generate_recommendation
from services.llm_service import generate_llm_response

def format_to_chatgpt_html(text: str) -> str:
    """Converts LLM raw markdown into structured HTML so Angular renders it beautifully."""
    # Convert bold **text** to <strong>text</strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Convert italic *text* to <em>text</em>
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Convert lists - item to HTML list layout
    text = re.sub(r'^\s*-\s+(.+)$', r'<li style="margin-bottom:6px; margin-left: 14px;">\1</li>', text, flags=re.MULTILINE)
    # Handle line breaks neatly instead of clumping text
    text = text.replace('\n', '<br>')
    # Wrap loose list items in a ul for spacing
    text = text.replace('</li><br><li', '</li><li')
    
    return text

def process_chat(message: str, user_id="default_user"):

    # 🧠 Emotion detection
    emotion = detect_emotion(message)

    # 💊 Clinical Recommendation based solely on emotion class
    therapy_recommendation = generate_recommendation(emotion)

    # 📚 RAG Context Retrieval (VECTOR SEARCH)
    rag_context = retrieve_context(message)

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

User base emotion: {emotion}
Emotion trend: {trend}

[Clinical Therapy Recommendation]: {therapy_recommendation}
{rag_context}

Conversation history:
{context}

User: {message}

Give a supportive, empathetic, and helpful response. If [Retrieved University Mental Health Resources] are provided above, ALWAYS naturally integrate those exact coping strategies or hotline numbers into your advice.

FORMATTING RULES:
1. Speak in a highly engaging, structured, ChatGPT-style manner.
2. Natively use HTML tags (e.g. <b>, <ul>, <li>, <br>) for formatting because your response will be rendered directly via innerHTML. Use HTML tables <table> if providing structured data.
3. Heavily use relevant emojis to make the response warm and readable. 
"""

    # 🤖 LLM call
    raw_response = generate_llm_response(prompt, emotion)
    
    # 🎨 Transform to ChatGPT UI specific HTML structure
    response = format_to_chatgpt_html(raw_response)

    # 💾 Save chat
    chat_id = save_chat(user_id, message, emotion, response)

    return {
        "chat_id": chat_id,
        "emotion": emotion,
        "response": response
    }