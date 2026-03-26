from transformers import pipeline

# Initialize the model globally (loads on startup)
# Using a lightweight, pre-trained emotion classification model
emotion_classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=1)

def detect_emotion(text: str) -> str:
    try:
        # result is a list of lists, e.g., [[{'label': 'sadness', 'score': 0.99}]]
        result = emotion_classifier(text)
        label = result[0][0]['label'].lower()
        
        # Map to our system's expected emotions
        if label in ["joy", "love"]:
            return "happy"
        elif label == "sadness":
            return "sad"
        elif label == "fear":
            return "anxiety"
        elif label == "anger":
            return "stress" # Mapping anger to stress for our academic context
        else:
            return "neutral"
            
    except Exception as e:
        print(f"Emotion detection error: {e}")
        # Fallback to simple heuristics if model fails
        text = text.lower()
        if "stress" in text or "pressure" in text: return "stress"
        if "sad" in text or "depressed" in text: return "sad"
        if "happy" in text: return "happy"
        if "anxious" in text: return "anxiety"
        return "neutral"