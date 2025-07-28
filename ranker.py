from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    """
    Helper to embed text using the sentence-transformers model.
    """
    # Handle empty or very short input defensively
    if not text or len(text.strip()) == 0:
        return np.zeros(model.get_sentence_embedding_dimension())
    return model.encode(text, convert_to_numpy=True)

def rank_sections(sections, persona, job_to_be_done):
    """
    Rank sections by semantic similarity to the persona+job query.

    Args:
        sections (list of dict): Extracted sections with 'text' key.
        persona (str): Persona description string.
        job_to_be_done (str): Job description string.

    Returns:
        List of sections dicts updated with 'importance_rank' (float),
        sorted in descending order of relevance.
    """
    query_text = (persona + " " + job_to_be_done).strip()

    if not query_text:
        # If no query provided, assign equal importance
        for sec in sections:
            sec["importance_rank"] = 0.0
        return sections

    # Embed query and section texts
    query_emb = embed_text(query_text)
    texts = [sec.get("text", "") for sec in sections]
    if not texts:
        return sections

    section_embs = model.encode(texts, convert_to_numpy=True)

    # Compute cosine similarity
    sims = cosine_similarity([query_emb], section_embs)[0]

    # Assign similarity score as importance_rank to each section
    for sec, sim in zip(sections, sims):
        sec["importance_rank"] = float(sim)

    # Sort by importance_rank descending
    ranked_sections = sorted(sections, key=lambda x: x["importance_rank"], reverse=True)
    return ranked_sections
