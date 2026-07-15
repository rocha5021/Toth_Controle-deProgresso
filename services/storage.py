"""
Cache local (JSON) dos dados reais buscados na TibiaData API - nao e
"dado do usuario" (equipamentos, metas, bestiary etc), so um cache de
API externa, por isso continua fora do SQLite (db/).
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

TRACKED_CACHE_FILE = DATA_DIR / "cache_tracked.json"


def load_tracked_cache():
    if TRACKED_CACHE_FILE.exists():
        with open(TRACKED_CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_tracked_cache(data):
    with open(TRACKED_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
