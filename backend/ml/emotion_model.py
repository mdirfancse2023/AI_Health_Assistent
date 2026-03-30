import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def detect_emotion(text: str) -> str:
    """Detect emotion using OpenRouter API"""
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""Analyze the emotion in this text and respond with ONLY one word from: happy, sad, anxiety, stress, or neutral.

Text: "{text}"

Response:"""
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 10
            }
        )
        
        if response.status_code == 200:
            emotion = response.json()["choices"][0]["message"]["content"].strip().lower()
            # Validate and map emotions
            valid_emotions = ["happy", "sad", "anxiety", "stress", "neutral"]
            return emotion if emotion in valid_emotions else "neutral"
        else:
            print(f"Emotion detection API error: {response.status_code}")
            return "neutral"
            
    except Exception as e:
        print(f"Emotion detection error: {e}")
        # Fallback to simple heuristics if API fails
        text = text.lower()
        if "stress" in text or "pressure" in text: return "stress"
        if "sad" in text or "depressed" in text: return "sad"
        if "happy" in text or "great" in text: return "happy"
        if "anxious" in text or "worry" in text: return "anxiety"
        return "neutral"