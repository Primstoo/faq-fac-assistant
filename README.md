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
« Je ne sais pas, vérifie auprès du service scolarité » si l'information n'est pas dans les
documents fournis. Pas d'exception, même si une réponse "plausible" existe.

## Architecture (v1, la plus simple possible)

```
Documents (PDF/texte) --> Chunking --> Embeddings --> Vector store
                                                            |
Question utilisateur --> Embedding --> Recherche similarité
                                                            |
                                              Chunks pertinents + question
                                                            |
                                                    LLM (Claude API)
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
│   └── app.py           # interface (v1 : script CLI, v2 : Streamlit)
├── notebooks/          # expérimentations rapides, non versionnées en prod
├── tests/               # tests sur chaque brique (surtout anti-hallucination)
├── requirements.txt
└── .env.example
```

## Roadmap v1 (dans l'ordre, chaque étape doit marcher avant de passer à la suivante)

1. **Ingestion** : lire 1 seul document texte/PDF et l'afficher en texte brut.
2. **Chunking** : découper ce texte en morceaux de taille raisonnable.
3. **Embeddings** : transformer les chunks en vecteurs.
4. **Vector store** : stocker les vecteurs, faire une recherche de similarité basique.
5. **Retrieval** : pour une question donnée, retrouver les chunks les plus pertinents.
6. **Generation** : envoyer chunks + question au LLM, forcer la citation de la source.
7. **Anti-hallucination** : tester des questions hors-sujet, vérifier que l'assistant refuse
   de répondre plutôt que d'inventer.
8. **Interface minimale** : script CLI d'abord, interface web ensuite (v2).

## Statut

🚧 En cours de construction — ingestion, chunking, embeddings et vector store faits et testés.
Prochaine étape : retrieval (seuil de similarité) puis generation (appel LLM).

## Licence

À définir (probablement MIT une fois le projet présentable).
