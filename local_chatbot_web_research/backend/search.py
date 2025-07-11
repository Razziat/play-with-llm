from dotenv import load_dotenv
load_dotenv()

import os, httpx, textwrap
from typing import List, Dict

API_KEY = os.getenv("SERPER_API_KEY")
if not API_KEY:
    raise RuntimeError("SERPER_API_KEY manquant dans .env")

_MIN_SNIPPET = 40
_BASE = "https://google.serper.dev"

def _trim(txt: str, width: int = 300) -> str:
    return textwrap.shorten((txt or "").strip(), width, placeholder=" …")

def _post(endpoint: str, payload: Dict) -> Dict:
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json",
    }
    url = f"{_BASE}/{endpoint.lstrip('/')}"
    with httpx.Client(timeout=15) as client:
        r = client.post(url, json=payload, headers=headers)
    print("DEBUG Serper", r.status_code)       # <——
    print("DEBUG payload", payload)            # <——
    try:
        print("DEBUG body", r.json())          # <——
    except Exception:
        print("DEBUG raw", r.text)
    r.raise_for_status()                       # lève si 4xx/5xx
    return r.json()

def _news_items(data: Dict, max_results: int) -> List[Dict]:
    items = []
    for n in data.get("news", [])[:max_results]:
        items.append(
            {
                "title": n.get("title", "").strip(),
                "url": n.get("link", "").strip(),
                "snippet": _trim(n.get("snippet") or n.get("title")),
            }
        )
    return items

def _web_items(data: Dict, max_results: int) -> List[Dict]:
    items = []
    for res in data.get("organic", [])[:max_results]:
        snippet = res.get("snippet") or res.get("title", "")
        items.append(
            {
                "title": res.get("title", "").strip(),
                "url": res.get("link", "").strip(),
                "snippet": _trim(snippet),
            }
        )
    return items

def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    1) Interroge /news (Google News) ;
    2) Si rien, interroge /search (Web).
    """
    # ---------- 1) Google News -------------------------------------------------
    news_resp = _post("news", {"q": query})
    results = [r for r in _news_items(news_resp, max_results) if len(r["snippet"]) >= _MIN_SNIPPET]

    # ---------- 2) Fallback Web ------------------------------------------------
    if not results:
        web_resp = _post("search", {"q": query})
        results = [r for r in _web_items(web_resp, max_results) if len(r["snippet"]) >= _MIN_SNIPPET]

    return results
