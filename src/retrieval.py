"""
Récupération des chunks pertinents pour une question donnée, à partir du vector store.
"""

from src.ingestion import read_document
from src.chunking import chunk_text
from src.vector_store import VectorStore


def build_store(path):
    """Construit un VectorStore indexé à partir d'un document source."""
    texte = read_document(path)
    chunks = chunk_text(texte)
    store = VectorStore()
    store.add_texts(chunks)
    return store


def retrieve(query, store, top_k=3, threshold=0.4):
    """
    Retourne les chunks pertinents pour query, ou une liste vide si aucun
    résultat ne dépasse le seuil de similarité (évite de transmettre un
    contexte non pertinent au LLM).
    """
    resultats = store.search(query, top_k)
    return [chunk for chunk, score in resultats if score > threshold]
