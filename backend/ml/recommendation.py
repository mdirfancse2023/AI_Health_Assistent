import random

# A structured, clinically grounded recommendation matrix mapped to the exact
# 6 emotional classes natively predicted by Hugging Face's 'distilbert-base-uncased-emotion'.
CLINICAL_RECOMMENDATION_MATRIX = {
    "sadness": [
        "Behavioral Activation: Start by setting one micro-goal today, like organizing your desk or taking a 10-minute walk outside to trigger a baseline dopamine release.",
        "Cognitive Reframing: Write down three negative thoughts you had today, and objectively challenge their factual accuracy on paper.",
        "Social Grounding: Reach out to a trusted peer or mentor, even just via text, to break the loop of academic isolation."
    ],
    "joy": [
        "Momentum Building: You are in an excellent cognitive state! Capitalize on this by tackling your hardest academic challenge today.",
        "Gratitude Journaling: Solidify positive neural pathways by writing down two specific things that brought you joy today.",
        "Social Reinforcement: Share your success or positive energy with a friend to reinforce communal bonding."
    ],
    "love": [
        "Connection Maintenance: Empathy and connection are high. Dedicate 20 minutes today to strictly non-academic socializing.",
        "Self-Compassion: Direct that empathy inward. Acknowledge your hard work and allow yourself a guilt-free evening of rest."
    ],
    "anger": [
        "Physiological De-escalation: Try the 'Mammalian Dive Reflex'. Splash freezing water on your face to forcibly slow your autonomic heart rate.",
        "Constructive Venting: Do a 'brain dump'. Write furiously on a piece of paper for 5 minutes, then literally tear it up to release kinetic frustration.",
        "Distance the Stressor: If you are angry at a specific assignment or grade, immediately step away. Do not email a professor or peer while in a heightened emotional state."
    ],
    "fear": [
        "Autonomic Regulation: Use Box Breathing (Inhale 4s, Hold 4s, Exhale 4s, Hold 4s) to directly combat the 'Fight or Flight' sympathetic nervous response.",
        "The 5-4-3-2-1 Grounding Method: Identify 5 things you see, 4 you can touch, 3 you hear, 2 you smell, and 1 you taste. This prevents anxiety spiraling.",
        "Probability Mapping: Ask yourself: 'What is the absolute worst case scenario?' Usually, explicitly naming the fear removes its psychological power."
    ],
    "surprise": [
        "Cognitive Processing: Unexpected events spike cortisol. Take 5 minutes to sit quietly and process how this new information changes your current academic plan.",
        "Adaptive Re-planning: If the surprise was negative (like an unexpected quiz), don't panic. Quickly sketch out a new 3-step recovery timeline."
    ]
}

def generate_recommendation(emotion: str) -> str:
    """
    Dynamically recommends an empirically-backed psychological coping mechanism 
    based on the localized Hugging Face Emotion classification.
    """
    normalized_emotion = emotion.lower().strip()
    
    if normalized_emotion in CLINICAL_RECOMMENDATION_MATRIX:
        # Randomly select a strategy from the specific emotional bucket to prevent conversational fatigue
        strategies = CLINICAL_RECOMMENDATION_MATRIX[normalized_emotion]
        return random.choice(strategies)
        
    return "I'm always here for you. Continuing to talk out your feelings with me is the best first step!"