import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_llm_response(prompt: str, emotion: str = ""):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt   # 🔥 FULL CONTEXT PROMPT
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        if response.status_code != 200:
            return "I'm here for you. Please tell me more."

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        print("LLM ERROR:", e)
        return "I'm here for you. Please tell me more."