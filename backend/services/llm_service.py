import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_llm_response(message: str, emotion: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a mental health assistant helping students.

Emotion: {emotion}
User: {message}

Respond in a supportive, short, and empathetic way.
"""

    data = {
        "model": "openai/gpt-3.5-turbo",   # 🔥 safer model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        if response.status_code != 200:
            return "I'm here for you. Please tell me more."

        result = response.json()

        # Safe extraction
        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        return "I'm here for you. Please tell me more."

    except Exception as e:
        print("LLM ERROR:", e)
        return "I'm here for you. Please tell me more."