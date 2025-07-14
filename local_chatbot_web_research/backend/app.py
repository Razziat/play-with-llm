# backend/app.py
import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from search import search_web
from llm import call_ollama, build_search_query

MAX_RESULTS = 3

app = FastAPI(title="Chatbot avec Internet")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────── classes ────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    use_search: bool = True

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

class ChatResponse(BaseModel):
    reply: str
    sources: List[SearchResult]

_TARGETS = {
    # mots-clés acceptés (singulier & pluriel, sans accent ET avec accent s’il existe)
    "source", "sources",
    "lien", "liens",
    "citation", "citations",
    "référence", "références",
    "reference", "references",
    "exemple", "exemples",
}

def detect_num_sources(text: str, cap: int = 10, radius: int = 5) -> int | None:
    """
    Renvoie le nombre (≤ cap) le plus proche d'un mot-clé.
    - 'radius' : nb maximum de mots autorisé entre le nombre et le mot-clé.
    - Ex. : « … Donne-moi 7 exemples concrets avec leurs sources » → 7
    """
    # 1) Découpe le texte en tokens : nombres OU séquences de lettres Unicode
    tokens = re.findall(r"\d+|[^\W\d_]+", text.lower(), flags=re.UNICODE)

    # 2) Indices des nombres et des mots-clés
    nums  = [(i, int(tok)) for i, tok in enumerate(tokens) if tok.isdigit()]
    keys  = [i for i, tok in enumerate(tokens) if tok in _TARGETS]

    if not nums or not keys:
        return None  # on n'a ni nombre ni mot-clé

    # 3) Cherche le couple (nombre, mot-clé) le plus proche
    best_val, best_dist = None, radius + 1
    for n_idx, val in nums:
        for k_idx in keys:
            dist = abs(n_idx - k_idx)
            if dist < best_dist:
                best_val, best_dist = val, dist

    # 4) Valide la distance et applique le plafond 'cap'
    if best_val is not None and best_dist <= radius:
        return min(best_val, cap) if best_val > 0 else None
    return None

# ──────── Route principale ───────────────────────────────────────────────────
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    user_prompt = req.message

     # ▼ 1) Déterminer combien de sources doivent être fournies
    requested = detect_num_sources(user_prompt)
    max_results = requested or MAX_RESULTS

    # 1) Générer la requête Web *seulement si use_search = True*
    if req.use_search:
        try:
            web_query = build_search_query(user_prompt)
            sources = search_web(web_query, max_results=max_results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur recherche : {e}")
    else:
        sources = []  # aucune recherche, pas de sources

    # 2) Appel LLM
    try:
        reply = call_ollama(sources, user_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur LLM : {e}")

    return ChatResponse(
        reply=reply,
        sources=[SearchResult(**s) for s in sources],
    )
