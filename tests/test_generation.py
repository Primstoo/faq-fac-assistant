"""
Tests anti-hallucination : vérifient que l'assistant refuse de répondre plutôt
que d'inventer quand aucun extrait pertinent ne lui est fourni.
"""

from src import generation
from src.generation import REFUS, generate_answer


def test_no_chunk_returns_the_refusal_message():
    assert generate_answer("Quelle est la capitale du Japon ?", []) == REFUS


def test_no_chunk_never_calls_the_api(monkeypatch):
    # Si aucun extrait n'est pertinent, la question ne doit pas partir au LLM :
    # c'est ce qui garantit le refus, et ça évite un appel facturé pour rien.
    def echec(*args, **kwargs):
        raise AssertionError("get_client() ne doit pas être appelé sans extrait.")

    monkeypatch.setattr(generation, "get_client", echec)
    assert generate_answer("Question hors-sujet", []) == REFUS


def test_the_system_prompt_states_the_refusal_rule():
    assert REFUS in generation.SYSTEM_PROMPT
