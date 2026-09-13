"""
Appel au LLM (API Anthropic, Claude) avec le contexte récupéré, prompt à citation
de source obligatoire et refus de répondre si l'information est absente.
"""

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-opus-5"

# Réponse unique en cas d'information absente. Définie une seule fois pour que
# le prompt et le court-circuit ci-dessous ne puissent pas diverger.
REFUS = "Je ne sais pas, vérifie auprès du service de scolarité."

SYSTEM_PROMPT = f"""Tu es un assistant qui répond aux questions de nouveaux étudiants
à partir UNIQUEMENT des extraits de documents fournis ci-dessous.

Règles strictes, sans exception :
- Ne réponds qu'à partir des extraits fournis, jamais de tes connaissances générales.
- Cite toujours l'extrait exact sur lequel tu t'appuies.
- Si l'information demandée n'est pas dans les extraits, réponds exactement :
  "{REFUS}"
Ne fais jamais d'exception à ces règles, même si une réponse plausible te vient à l'esprit."""

_client = None


def get_client():
    """Crée le client Anthropic une seule fois, à la demande (pas au chargement du module)."""
    global _client
    if _client is None:
        _client = anthropic.Anthropic()  # lit ANTHROPIC_API_KEY dans l'environnement
    return _client


def generate_answer(question, chunks):
    """
    Envoie la question et les chunks pertinents à Claude. Si aucun chunk n'est
    fourni (rien de pertinent trouvé par retrieval.py), renvoie directement le
    refus, sans appeler l'API.
    """
    if not chunks:
        return REFUS

    contexte = "\n\n---\n\n".join(chunks)
    response = get_client().messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Extraits de documents :\n\n{contexte}\n\nQuestion : {question}",
        }],
    )
    return next((block.text for block in response.content if block.type == "text"), "")
