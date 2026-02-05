# FILE: app/services/similarity_engine.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityEngine:

    # ----------------------------------------------------------
    # Single similarity score (resume vs one JD)
    # ----------------------------------------------------------
    def calculate_similarity(self, resume_emb, jd_emb):
        """
        Calculates cosine similarity between two embedding vectors.
        Ensures stability & normalization.
        Returns value between 0 and 1.
        """
        if resume_emb is None or jd_emb is None:
            return 0.0

        try:
            # Convert to numpy arrays
            r_vec = np.array(resume_emb).reshape(1, -1)
            jd_vec = np.array(jd_emb).reshape(1, -1)

            # Normalize vectors for stable similarity
            r_norm = r_vec / np.linalg.norm(r_vec)
            jd_norm = jd_vec / np.linalg.norm(jd_vec)

            score = cosine_similarity(r_norm, jd_norm)[0][0]
            score = max(0.0, min(1.0, float(score)))   # clamp 0–1

            return score
        except Exception:
            return 0.0

    # ----------------------------------------------------------
    # Batch similarity → MANY resumes vs one JD
    # ----------------------------------------------------------
    def batch_similarity(self, resume_embeddings, jd_emb):
        """
        Calculates similarity scores for multiple resume embeddings
        against a single job description embedding.
        Returns list of scores.
        """
        if jd_emb is None or len(resume_embeddings) == 0:
            return []

        scores = []
        for emb in resume_embeddings:
            score = self.calculate_similarity(emb, jd_emb)
            scores.append(score)

        return scores
