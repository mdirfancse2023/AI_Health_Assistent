import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

import json

def generate_llm_stream(prompt: str, emotion: str = ""):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "stream": True,
        "messages": [
            {
                "role": "user",
                "content": prompt   # 🔥 FULL CONTEXT PROMPT
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)

        if response.status_code != 200:
            print("STATUS:", response.status_code, response.text)
            yield "I'm here for you. Please tell me more."
            return

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    json_str = decoded_line[6:]
                    if json_str.strip() == "[DONE]":
                        break
                    try:
                        chunk_data = json.loads(json_str)
                        if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                            delta = chunk_data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except Exception as e:
                        print("Stream parse err:", e)
                        pass

    except Exception as e:
        print("LLM ERROR:", e)
        yield "I'm here for you. Please tell me more."