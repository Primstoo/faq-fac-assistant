# faq-fac-assistant

Chatbot RAG (Retrieval-Augmented Generation) qui répond aux questions des nouveaux étudiants
d'une faculté (règlement pédagogique, procédures, FAQ) en se basant **uniquement** sur des
documents officiels, avec citation systématique de la source et refus de répondre si
l'information n'est pas trouvée dans les documents.

## Pourquoi ce projet

Beaucoup d'échecs académiques en première année viennent d'un manque d'accès à la bonne
information, pas d'un manque de compétence. Ce projet teste si un assistant RAG simple et
fiable peut combler ce manque, sans jamais halluciner de réponse.

## Règle non négociable

L'assistant doit **toujours** citer sa source exacte (document + section), et répondre
« Je ne sais pas, vérifie auprès du service de scolarité » si l'information n'est pas dans les
documents fournis. Pas d'exception, même si une réponse "plausible" existe.

Concrètement, cette règle est appliquée à deux endroits :

1. `retrieval.py` écarte les chunks dont la similarité est sous un seuil ;
2. `generation.py` renvoie directement le refus quand il ne reste aucun chunk, **sans appeler
   le LLM** — le modèle ne peut donc pas inventer une réponse sur une question hors-sujet.

## Architecture (v1, la plus simple possible)

```
Documents (PDF/texte) --> Chunking --> Embeddings --> Vector store
                                                            |
Question utilisateur --> Embedding --> Recherche similarité
                                                            |
                                              Chunks pertinents + question
                                                            |
                                                    LLM (API Claude)
                                                            |
                                          Réponse + citation de la source
```

## Structure du dossier

```
faq-fac-assistant/
├── data/
│   ├── raw/          # documents sources (PDF, texte) tels que récupérés
│   └── processed/     # chunks découpés, prêts à être vectorisés
├── src/
│   ├── ingestion.py    # lecture des documents (PDF/texte -> texte brut)
│   ├── chunking.py     # découpage du texte en morceaux exploitables
│   ├── embeddings.py   # transformation des chunks en vecteurs
│   ├── vector_store.py # stockage + recherche par similarité
│   ├── retrieval.py    # récupération des chunks pertinents pour une question
│   ├── generation.py   # appel au LLM avec contexte + citation obligatoire
│   └── app.py           # interface CLI
├── tests/               # tests unitaires (dont les tests anti-hallucination)
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env   # puis renseigner ANTHROPIC_API_KEY
```

Le modèle d'embeddings (`all-MiniLM-L6-v2`, ~90 Mo) tourne en local et se télécharge
automatiquement au premier lancement. Seule la génération de la réponse finale passe par
l'API Claude.

## Utilisation

```bash
python -m src.app                          # utilise data/raw/exemple.txt
python -m src.app chemin/vers/document.pdf
```

L'assistant indexe le document, puis attend les questions ; `quit` pour sortir.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

12 tests couvrent le découpage (taille, chevauchement, aucune perte de texte, garde-fou sur
`overlap >= chunk_size`), la lecture des documents et le comportement anti-hallucination
(refus renvoyé **sans appel API** quand aucun extrait n'est pertinent — c'est le test qui
garantit la règle non négociable ci-dessus).

7 tests supplémentaires couvrent le vector store et le seuil de recherche. Ils chargent le
modèle d'embeddings et sont donc ignorés automatiquement (`pytest.importorskip`) si
`sentence-transformers` n'est pas installé, pour que la suite reste exécutable rapidement sans
télécharger le modèle.

Aucun test n'appelle l'API Claude : la suite tourne sans clé et sans coût.

## Roadmap v1 (dans l'ordre, chaque étape doit marcher avant de passer à la suivante)

1. ~~**Ingestion** : lire 1 seul document texte/PDF et l'afficher en texte brut.~~
2. ~~**Chunking** : découper ce texte en morceaux de taille raisonnable.~~
3. ~~**Embeddings** : transformer les chunks en vecteurs.~~
4. ~~**Vector store** : stocker les vecteurs, faire une recherche de similarité basique.~~
5. ~~**Retrieval** : pour une question donnée, retrouver les chunks les plus pertinents.~~
6. ~~**Generation** : envoyer chunks + question au LLM, forcer la citation de la source.~~
7. ~~**Anti-hallucination** : tester des questions hors-sujet, vérifier que l'assistant refuse
   de répondre plutôt que d'inventer.~~
8. ~~**Interface minimale** : script CLI.~~

## Statut

Les 8 étapes de la roadmap sont écrites et câblées : la chaîne complète (ingestion → chunking
→ embeddings → vector store → retrieval → génération) est accessible depuis le CLI, et la
règle de refus est couverte par des tests qui passent.

Reste à faire avant de parler de v1 « validée » : le run de bout en bout contre l'API Claude
avec une vraie clé, sur un vrai règlement, et le réglage du seuil qui en découlera.

Limites connues et assumées :

- La citation de source se limite à l'extrait transmis au modèle : les chunks ne portent pas
  encore de métadonnée (document d'origine, numéro d'article), donc l'assistant cite le texte
  mais pas sa référence précise. C'est la prochaine étape.
- Le seuil de similarité (0.4) a été réglé à la main sur un seul document ; il demanderait
  d'être calibré sur un vrai corpus.
- Le vector store est en mémoire : l'index est reconstruit à chaque démarrage.
- Interface web (Streamlit) prévue en v2.

## Licence

MIT — voir [LICENSE](LICENSE).
