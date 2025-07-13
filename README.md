# Mon dépôt Chatbot IA

Ce dépôt principal regroupe plusieurs projets et documents relatifs à la partie pratique et théorique de votre Chatbot IA :

| Dossier                       | Contenu                                                                      |
| ----------------------------- | ---------------------------------------------------------------------------- |
| `local_chatbot_web_research/` | Projet **Chatbot IA Web** : backend FastAPI + frontend React, RAG Web        |
| `local_vlm_chatbot/`          | Prototype **VLM Chatbot** : script Python + interface Tkinter pour Ollama    |
| `questions_theoriques/`       | Documents et réponses aux **questions théoriques**                           |

---

## local\_chatbot\_web\_research

Contient le Chatbot IA Web complet :

1. **backend/** : API FastAPI, recherche Serper.dev, RAG via Ollama
2. **frontend/** : application React (Create React App)

Pour les instructions d’installation et d’exécution, référez-vous au **README** situé dans ce dossier.

---

## local\_vlm\_chatbot

Prototype simple d’intégration d’un **Vision–Language Model** (VLM) :

* **script principal** : sélection d’image (Tkinter) + appel CLI Ollama

Pour les instructions d’installation et d’exécution, référez-vous au **README** situé dans ce dossier.

---

## questions\_theoriques

Dossier contenant les réponses et documents produits pour la partie théorique :

* Architecture Azure, déploiement, sécurité, CI/CD
* Pipeline RAG, graphe vectoriel vs index vectoriel, etc.

Chaque fichier y est au format Markdown.

---

## Organisation du dépôt

```bash
.
├── local_chatbot_web_research/
│   ├── backend/
│   └── frontend/
├── local_vlm_chatbot/
└── questions_theoriques/
```

---
