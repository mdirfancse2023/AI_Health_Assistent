import os
import json
import torch
from transformers import AutoTokenizer, AutoModel

# Load lightweight embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

RESOURCE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "resources.json")

knowledge_base = []
knowledge_embeddings = None

def load_and_embed_knowledge_base():
    """Loads the JSON resources and pre-computes their tensor embeddings on module initialization."""
    global knowledge_base, knowledge_embeddings
    
    if not os.path.exists(RESOURCE_FILE):
        print(f"RAG WARNING: Knowledge base not found at {RESOURCE_FILE}")
        return

    with open(RESOURCE_FILE, "r") as f:
        knowledge_base = json.load(f)

    if not knowledge_base:
        return

    # Extract text content for embedding
    texts = [item["content"] for item in knowledge_base]
    
    # Compute embeddings in a batch
    print(f"RAG INIT: Computing embeddings for {len(texts)} resources...")
    knowledge_embeddings = get_embedding(texts)
    print("RAG INIT: Embeddings computed successfully.")

def get_embedding(texts):
    """Generates standard dense embeddings using the transformer model."""
    if isinstance(texts, str):
        texts = [texts]
        
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    # Standard Mean Pooling: average the token embeddings, ignoring attention mask
    token_embeddings = outputs.last_hidden_state
    attention_mask = inputs['attention_mask']
    
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    embeddings = sum_embeddings / sum_mask
    return embeddings

def retrieve_context(query: str, top_k: int = 1) -> str:
    """
    Given a user query, calculates cosine similarity against the pre-computed 
    knowledge base embeddings and returns the most relevant resource content.
    """
    if knowledge_embeddings is None or len(knowledge_base) == 0:
        return ""
        
    query_embedding = get_embedding([query])
    
    # Calculate Cosine Similarity: query vs all knowledge base embeddings
    cos_scores = torch.nn.functional.cosine_similarity(query_embedding, knowledge_embeddings)
    
    # Get top K indices
    top_results = torch.topk(cos_scores, k=min(top_k, len(knowledge_base)))
    
    best_matches = []
    # threshold for relevance (preventing irrelevant RAG injections)
    for score, idx in zip(top_results.values, top_results.indices):
        if score.item() > 0.3:  # Only inject if structurally relevant
            best_matches.append(knowledge_base[idx.item()]["content"])
            
    if best_matches:
        formatted_context = "\n---\n".join(best_matches)
        return f"[Retrieved University Mental Health Resources]:\n{formatted_context}"
    
    return ""

# Initialize embeddings immediately when this module is imported by FastAPI
load_and_embed_knowledge_base()
