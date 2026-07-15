"""
Cache local (JSON) das URLs de imagem resolvidas via wiki_images.py, pra
nao ficar batendo na TibiaWiki toda vez que o app abre. So refaz a
resolucao quando um nome novo aparece no cache.
"""
import json
from pathlib import Path

from services import wiki_images

CACHE_FILE = Path(__file__).parent.parent / "data" / "image_cache.json"


def _load():
    if CACHE_FILE.exists():
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_image_url(name, kind="creature"):
    """Retorna a URL da imagem (ou None) para o nome dado, usando cache local."""
    cache = _load()
    key = f"{kind}:{name}"
    if key in cache:
        return cache[key]
    url = wiki_images.resolve_image(name, kind)
    cache[key] = url
    _save(cache)
    return url


def warm_cache(names, kind="creature", progress=None):
    """Resolve e cacheia uma lista de nomes de uma vez (usado no startup/build)."""
    cache = _load()
    for i, name in enumerate(names):
        key = f"{kind}:{name}"
        if key not in cache:
            cache[key] = wiki_images.resolve_image(name, kind)
        if progress:
            progress(i, len(names))
    _save(cache)
