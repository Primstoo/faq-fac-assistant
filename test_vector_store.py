from src.vector_store import VectorStore

phrases = [
    "L'inscription administrative est obligatoire chaque année.",
    "Les étudiants absents doivent justifier leur absence.",
    "Puisses Dieu nous pardonne d'avoir penser que nous etions meilleurs qu'eux.",
]

store = VectorStore()
store.add_texts(phrases)

resultats = store.search("Est-ce que je dois justifier si je suis absent ?", top_k=2)
for r in resultats:
    print(r)
