"""
embeddings.py

Transformation du texte en vecteur numérique (embedding), pour pouvoir
ensuite comparer des textes entre eux par similarité (vector_store.py fera cette
comparaison). Modèle utilisé : all-MiniLM-L6-v2 (sentence-transformers), gratuit,
tourne en local, ~90 Mo, télécharge une seule fois puis mis en cache sur le disque.
"""

from sentence_transformers import SentenceTransformer

_model = None


def load_model():
    """Charge le modèle une seule fois et le réutilise (évite de le recharger à chaque appel)."""
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts):
    """
    Transforme une liste de textes (ex: les chunks) en tableau de vecteurs numpy.
    Retourne un tableau de forme (nombre_de_textes, 384).
    """
    model = load_model()
    return model.encode(texts, convert_to_numpy=True)


def embed_query(text):
    """Transforme une seule question en vecteur (même modèle, même dimension que embed_texts)."""
    return embed_texts([text])[0]
