"""
Tests du seuil de similarité. Ils chargent le modèle d'embeddings
(sentence-transformers) : ils sont ignorés si la dépendance n'est pas installée.
"""

import pytest

pytest.importorskip("sentence_transformers")

from src.retrieval import retrieve  # noqa: E402
from src.vector_store import VectorStore  # noqa: E402

PHRASES = [
    "L'inscription administrative est obligatoire chaque année universitaire.",
    "Les absences non justifiées au-delà de trois par module bloquent l'accès à l'examen.",
    "La session de rattrapage ne concerne que les modules non validés.",
]


@pytest.fixture(scope="module")
def store():
    store = VectorStore()
    store.add_texts(PHRASES)
    return store


def test_relevant_question_returns_chunks(store):
    resultats = retrieve("Puis-je repasser un module que je n'ai pas validé ?", store)
    assert resultats


def test_off_topic_question_returns_nothing(store):
    # Rien au-dessus du seuil : retrieval ne transmet aucun contexte au LLM,
    # qui répondra donc par le refus plutôt que d'inventer.
    resultats = retrieve("Quelle est la recette de la tarte aux pommes ?", store)
    assert resultats == []


def test_top_k_limits_the_number_of_chunks(store):
    resultats = retrieve("inscription", store, top_k=1, threshold=0.0)
    assert len(resultats) == 1
