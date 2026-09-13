"""
Tests du stockage vectoriel et de la recherche par similarité. Ils chargent le
modèle d'embeddings : ignorés si sentence-transformers n'est pas installé.
"""

import pytest

pytest.importorskip("sentence_transformers")

from src.vector_store import VectorStore  # noqa: E402

PHRASES = [
    "L'inscription administrative est obligatoire chaque année universitaire.",
    "Les étudiants absents doivent justifier leur absence sous 48 heures.",
    "Le chat dort sur le canapé.",
]


@pytest.fixture(scope="module")
def store():
    store = VectorStore()
    store.add_texts(PHRASES)
    return store


def test_search_returns_chunk_score_pairs(store):
    resultats = store.search("Que faire en cas d'absence ?", top_k=2)
    assert len(resultats) == 2
    for chunk, score in resultats:
        assert chunk in PHRASES
        assert 0.0 <= score <= 1.0


def test_closest_phrase_comes_first(store):
    resultats = store.search("Dois-je justifier une absence ?", top_k=3)
    assert resultats[0][0] == PHRASES[1]


def test_results_are_sorted_by_decreasing_score(store):
    scores = [score for _, score in store.search("inscription", top_k=3)]
    assert scores == sorted(scores, reverse=True)


def test_off_topic_phrase_scores_lowest(store):
    resultats = store.search("Quand dois-je m'inscrire à la faculté ?", top_k=3)
    assert resultats[-1][0] == PHRASES[2]
