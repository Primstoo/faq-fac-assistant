"""
embeddings.py

BROUILLON écrit par Claude pendant une session tardive — PAS ENCORE relu/compris/validé
par [toi]. À décortiquer ensemble ligne par ligne avant de le considérer comme acquis
(règle du CLAUDE.md : tu dois pouvoir défendre chaque ligne en entretien).

Rôle du module : transformer du texte en vecteur numérique (embedding), pour pouvoir
ensuite comparer des textes entre eux par similarité (vector_store.py fera cette
comparaison). Modèle utilisé : all-MiniLM-L6-v2 (sentence-transformers), gratuit,
tourne en local, ~90 Mo, télécharge une seule fois puis mis en cache sur le disque.

Points à discuter ensemble demain :
- Pourquoi charger le modèle une seule fois (variable globale _model) plutôt qu'à
  chaque appel de embed_texts ?
- Pourquoi convert_to_numpy=True plutôt que de garder le format par défaut (tensor) ?
- Que contient concrètement le tableau retourné (dimensions, type) ?
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
