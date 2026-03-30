import os
import json
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
RESOURCE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "resources.json")

knowledge_base = []

def load_knowledge_base():
    """Load the JSON resources"""
    global knowledge_base
    
    if not os.path.exists(RESOURCE_FILE):
        print(f"RAG WARNING: Knowledge base not found at {RESOURCE_FILE}")
        return

    with open(RESOURCE_FILE, "r") as f:
        knowledge_base = json.load(f)
    print(f"RAG INIT: Loaded {len(knowledge_base)} resources")

def retrieve_context(query: str, top_k: int = 1) -> str:
    """
    Use OpenRouter API to find the most relevant resources from knowledge base
    """
    if not knowledge_base:
        return ""
        
    try:
        # Create a prompt to find the most relevant resource
        resources_text = "\n\n".join([
            f"Resource {i+1}: {item.get('title', 'Unknown')}\nContent: {item['content'][:200]}..."
            for i, item in enumerate(knowledge_base[:5])  # Limit to top 5 to keep context small
        ])
        
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
                        "content": f"""Given these university mental health resources:

{resources_text}

User query: "{query}"

Return ONLY the number (1-5) of the most relevant resource. Just the number, nothing else."""
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 5
            }
        )
        
        if response.status_code == 200:
            try:
                result = response.json()["choices"][0]["message"]["content"].strip()
                idx = int(result) - 1
                if 0 <= idx < len(knowledge_base):
                    content = knowledge_base[idx]["content"]
                    return f"[Retrieved Mental Health Resource: {knowledge_base[idx].get('title', 'Resource')}]\n{content}"
            except (ValueError, IndexError, KeyError):
                pass
        
        return ""
            
    except Exception as e:
        print(f"RAG retrieval error: {e}")
        return ""

# Initialize knowledge base immediately when this module is imported by FastAPI
load_knowledge_base()

