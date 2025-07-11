# backend/llm.py
import os
import re
import subprocess
from datetime import datetime
from typing import List, Dict

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")  # par défaut modèle 8 b

# ▸ 2.1 — Prompt système pour la réponse finale
SYSTEM_PROMPT = (
    "Tu es un assistant répondant en français à partir des extraits fournis."
    "Utilise ces extraits pour rédiger une réponse concise et claire. "
    "Si vraiment aucune information pertinente n'apparaît dans les extraits, "
    "alors dis : « Je n'ai pas trouvé d'informations pertinentes. » "
    "Sinon, référence les sources avec des numéros [1], [2]…"
)

def _simplify(q: str, limit: int = 8) -> str:
    """Supprime | et guillemets, réduit à <limit> mots."""
    q = re.sub(r'[|\"“”«»]+', ' ', q)
    words = q.split()
    return " ".join(words[:limit])

# ▸ 2.2 — FABRIQUER une requête Web concise -------------------------------------------------
def build_search_query(user_prompt: str) -> str:
    """
    Demande au modèle de convertir la question utilisateur
    en une requête de recherche Web brève et pertinente.
    Il doit répondre sur une seule ligne, sans guillemets.
    """
    prompt = (
        "Génère une requête de recherche Web concise pour répondre à la question suivante : "
        "Réponds seulement par la requête, sans aucune phrase d’explication.\n\n"
        f"Question : {user_prompt}\nRequête :"
    )

    try:
        proc = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        query = proc.stdout.splitlines()[0].strip()
        return _simplify(query) or _simplify(user_prompt)
    except subprocess.CalledProcessError as e:
        raise RuntimeError((e.stderr or e.stdout).strip())

# ▸ 2.3 — RÉPONDRE à l’utilisateur ------------------------------------------------------------
def call_ollama(sources: List[Dict[str, str]], user_prompt: str) -> str:
    today = datetime.utcnow().strftime("%Y-%m-%d")

    # Concatène titre, URL et snippet
    blocks = [
        f"Titre : {s['title']}\nURL : {s['url']}\nExtrait : {s['snippet']}"
        for s in sources
    ]
    sources_block = "\n---\n".join(blocks)

    full_prompt = (
        f"{SYSTEM_PROMPT}\nDate : {today}\n\n"
        f"SOURCES :\n{sources_block}\n\n"
        f"Question : {user_prompt}\nRéponse :"
    )

    try:
        proc = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=full_prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError((e.stderr or e.stdout).strip())
