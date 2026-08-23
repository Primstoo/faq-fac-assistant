"""
Stockage en mémoire des chunks et de leurs vecteurs, avec recherche par
similarité cosinus pour retrouver les chunks les plus proches d'une question.
"""

import numpy as np
from src.embeddings import embed_texts, embed_query


class VectorStore:
    def __init__(self):
        self.chunks = []
        self.vectors = None

    def add_texts(self, chunks):
        """Calcule et stocke les  vecteurs de la liste de chunks donnée."""
        self.chunks = chunks
        self.vectors = embed_texts(chunks)

    def search(self, query, top_k=3):
        """Retourne les top_k chunks les plus proches en sens de la question."""
        query_vector = embed_query(query)
        similarities = self._cosine_similarities(query_vector)
        best_indices = np.argsort(similarities)[::-1][:top_k]
        return [self.chunks[i] for i in best_indices]

    def _cosine_similarities(self, query_vector):
        """Similarité cosinus entre query_vector et chaque vecteur stocké."""
        dot_products = self.vectors @ query_vector
        norms = np.linalg.norm(self.vectors, axis=1) * np.linalg.norm(query_vector)
        return dot_products / norms
