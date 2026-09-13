"""
Point d'entrée en ligne de commande : indexe un document, puis répond aux
questions posées au clavier jusqu'à "quit".

Usage :
    python -m src.app [chemin/vers/document.txt]
"""

import sys

from src.generation import generate_answer
from src.retrieval import build_store, retrieve

DOCUMENT_PAR_DEFAUT = "data/raw/exemple.txt"


def main():
    chemin = sys.argv[1] if len(sys.argv) > 1 else DOCUMENT_PAR_DEFAUT

    print(f"Indexation de {chemin} ...")
    store = build_store(chemin)
    print("Prêt. Pose une question, ou tape 'quit' pour quitter.\n")

    while True:
        question = input("> ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue

        chunks = retrieve(question, store)
        print(f"\n{generate_answer(question, chunks)}\n")


if __name__ == "__main__":
    main()
