from src.embeddings import embed_texts

phrases = [
    "L'inscription administrative est obligatoire chaque année.",
    "Les étudiants absents doivent justifier leur absence.",
    "Le chat dort sur le canapé.",
]

vecteurs = embed_texts(phrases)
print("Shape :", vecteurs.shape)
print("Début du premier vecteur :", vecteurs[0][:5])
