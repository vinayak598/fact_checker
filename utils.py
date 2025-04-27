# utils.py
from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_article_texts(articles, claim):
    # Encode claim once
    claim_embedding = model.encode(claim, convert_to_tensor=True)
    texts = []

    for article in articles:
        # Combine title, description, and content
        text = f"{article['title']}. {article.get('description', '')} {article.get('content', '')}"
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # Encode sentences
        sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

        # Calculate similarities
        similarities = util.pytorch_cos_sim(claim_embedding, sentence_embeddings)[0]

        # Keep sentences with similarity > 0.4
        best_sentences = [
            sentence for sentence, sim in zip(sentences, similarities) if sim.item() > 0.4
        ]

        if best_sentences:
            texts.append(". ".join(best_sentences))

    return texts
