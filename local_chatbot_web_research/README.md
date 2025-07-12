# Chatbot IA avec Internet

Backend FastAPI · Frontend React

Ce dépôt contient :

| Dossier     | Contenu principal                             |
| ----------- | --------------------------------------------- |
| `backend/`  | API FastAPI, recherche Serper.dev, LLM Ollama |
| `frontend/` | Application React (Create React App)          |

---

## 1. Prérequis

| Outil                 | Version conseillée           |
| --------------------- | ---------------------------- |
| **Python**            |  ≥ 3.10                      |
| **Node.js**           |  ≥ 18                        |
| **npm / pnpm / yarn** | dernière LTS                 |
| **Ollama**            | installé & modèle téléchargé |

---

## 2. Cloner le projet

```bash
git clone https://github.com/<votre‑org>/<repo>.git
cd <repo>
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
npm start     # lance CRA sur http://localhost:3000
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

