# Chatbot IA avec Internet

Backend FastAPI · Frontend React

Ce dépôt contient :

| Dossier     | Contenu principal                             |
| ----------- | --------------------------------------------- |
| `backend/`  | API FastAPI, recherche Serper.dev, LLM Ollama |
| `frontend/` | Application React (Vite)                      |

---

## 1. Prérequis

| Outil                 | Version conseillée           |
| --------------------- | ---------------------------- |
| **Python**            |  ≥ 3.10                      |
| **Node.js**           |  ≥ 18                        |
| **npm / pnpm / yarn** | dernière LTS                 |
| **Ollama**            | installé & modèle llama3.2:3b|

---

## 2. Cloner le projet

```bash
git clone git@github.com:Razziat/play-with-llm.git ou https://github.com/Razziat/play-with-llm.git
cd play_with_llm/local_chatbot_web_research
```

---

## 3. Obtenir une clé Serper.dev

1. Créez un compte gratuit sur [https://serper.dev/](https://serper.dev/).
2. Copiez votre **API Key** depuis le tableau de bord.

---

## 4. Variables d’environnement (backend)

Dans `backend/`, créez un fichier **`.env`** :

```
SERPER_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxx"    # clé obtenue sur serper.dev
```

> Pour utiliser un autre modèle Ollama que celui par défaut, ouvrez **`backend/llm.py`**, ligne 8, et remplacez la valeur dans la variable `OLLAMA_MODEL`.
> Pour avoir de bons résultats il est conseillé d'utiliser un modèle de 8b de paramètres. Le modèle par défaut est de 3b de paramètres mais ne donne pas de très bons résultats.

---

## 5. Installation & lancement

Ouvrez **deux terminaux** :

### Terminal 1 – Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate           # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --reload  # API sur http://127.0.0.1:8000
````

\### Terminal 2 – Frontend

```bash
cd frontend
npm install
npm run dev     # lance CRA sur http://localhost:3000
```

---

## 6. Utilisation

1. Ouvrez **[http://localhost:3000](http://localhost:3000)**.
2. Saisissez votre question dans la zone de discussion.
3. (Optionnel) décochez « Activer la recherche Web » pour interroger uniquement le modèle.
4. Les sources utilisées s’affichent sous la réponse.

> Vous pouvez demander un nombre précis de sources :
> *« Donne‑moi **5 sources** sur… »* ajustera dynamiquement la recherche. Par défaut, le modèle vous donnera 3 sources.

---

