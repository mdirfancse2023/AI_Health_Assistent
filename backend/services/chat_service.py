import json
from db.chat_repository import save_chat, get_recent_chats, get_emotion_summary
from ml.emotion_model import detect_emotion
from ml.rag_model import retrieve_context
from ml.recommendation import generate_recommendation
from services.llm_service import generate_llm_stream

def process_chat_stream(message: str, user_id="default_user"):

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

    # 🧠 ELITE PROMPT ENGINEERING
    prompt = f"""
You are an elite, highly advanced AI Clinical Mental Health Assistant designed specifically to help university students. Your goal is to sound as intelligent, articulate, and empathetic as a Master's-level therapist or high-end life coach (like ChatGPT-4).

You must organically synthesize the following backend data streams constraint into your response smoothly:
- User's Current Emotion Vector: {emotion}
- User's Historical Emotion Trend: {trend}
- Required [Clinical Therapy Recommendation]: {therapy_recommendation}
{rag_context}

Conversation History Context:
{context}

Current Student Message: {message}

OUTPUT RULES (CRITICAL):
1. Give a deeply nuanced, empathetic, and highly intelligent psychological response. DO NOT sound like a generic robot.
2. Validate their feelings deeply utilizing cognitive behavioral therapy (CBT) conversational principles.
3. If [Retrieved University Mental Health Resources] or [Clinical Therapy] are provided above, explicitly integrate them flawlessly into your reasoning. Explain *why* these mechanisms biologically or psychologically work for their specific emotion.
4. Structure your response elegantly like an advanced AI: heavily use native Markdown, bolding key insights, breaking long text into very readable logical bullet points, and using relevant emojis to maintain warmth.
5. Provide immediately actionable, step-by-step guidance.
"""

    # 🤖 LLM streaming call
    full_response = ""
    for chunk in generate_llm_stream(prompt, emotion):
        full_response += chunk
        # Yield Server-Sent Event formatted chunks
        yield f"data: {json.dumps({'chunk': chunk})}\n\n"

    # 💾 Save full completed chat to database
    chat_id = save_chat(user_id, message, emotion, full_response)

    # Yield final metadata so frontend can hook up feedback buttons
    yield f"data: {json.dumps({'chat_id': chat_id, 'emotion': emotion})}\n\n"
    
    # Indicate end of stream
    yield "data: [DONE]\n\n"