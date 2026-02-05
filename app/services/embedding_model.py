# FILE: app/services/embedding_model.py

from sentence_transformers import SentenceTransformer
import torch

class EmbeddingModel:
    def __init__(self):
        """
        Loads the SBERT model with automatic device selection (CPU/GPU).
        Also initializes a cache dictionary to avoid recomputing embeddings.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load SBERT (fast + accurate + lightweight)
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device=self.device
        )

        # Cache for repeated text (boosts speed)
        self.cache = {}

    # ----------------------------------------------------------
    # Single sentence embedding
    # ----------------------------------------------------------
    def get_embedding(self, text: str):
        """
        Returns embedding for a single text input.
        Uses caching for speed optimization.
        """
        if not text or not isinstance(text, str):
            return None

        # Cache hit
        if text in self.cache:
            return self.cache[text]

        try:
            emb = self.model.encode(
                text,
                convert_to_numpy=True,
                device=self.device
            )
            self.cache[text] = emb
            return emb
        except Exception:
            return None

    # ----------------------------------------------------------
    # Batch Embeddings (FAST for multi-resume)
    # ----------------------------------------------------------
    def get_batch_embeddings(self, text_list):
        """
        Generates embeddings for multiple texts at once.
        Much faster than single encoding.
        """
        try:
            embeddings = self.model.encode(
                text_list,
                convert_to_numpy=True,
                batch_size=16,
                device=self.device
            )
            return embeddings
        except Exception:
            return []
