import torch
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def verify_claim(claim, article_texts):
    # Encode the claim and articles into embeddings (convert to tensor if not already)
    claim_embedding = model.encode(claim, convert_to_tensor=True).unsqueeze(0)  # Add batch dimension
    
    results = []
    
    for article in article_texts:
        article_embedding = model.encode(article, convert_to_tensor=True).unsqueeze(0)  # Add batch dimension
        
        # Compute cosine similarity between claim_embedding and article_embedding
        similarity = torch.cosine_similarity(claim_embedding, article_embedding).item()
        results.append(similarity)
    
    avg_score = sum(results) / len(results) if results else 0

    if avg_score > 0.7:
        verdict = "✅ Likely True"
    elif avg_score < 0.4:
        verdict = "❌ Likely False"
    else:
        verdict = "⚠️ Needs More Context"

    return verdict, avg_score
