"""
Cache local (JSON) das URLs de imagem resolvidas via wiki_images.py, pra
nao ficar batendo na TibiaWiki toda vez que o app abre.

IMPORTANTE: resolver uma imagem nova bate na rede (pode ser lento em lote -
645 criaturas levam minutos). Por isso views/controllers usados durante a
navegacao normal do usuario devem usar `get_cached_image_url` (so le o
cache, nunca resolve on-demand). A resolucao de verdade acontece uma vez,
em lote, via `warm_cache` (rodado por um script/thread de preparo, nao no
caminho de renderizacao da tela).
"""
import json
import threading
from pathlib import Path

from services import wiki_images

CACHE_FILE = Path(__file__).parent.parent / "data" / "image_cache.json"

_memory_cache = None
_lock = threading.Lock()


def _load():
    global _memory_cache
    if _memory_cache is None:
        if CACHE_FILE.exists():
            with open(CACHE_FILE, encoding="utf-8") as f:
                _memory_cache = json.load(f)
        else:
            _memory_cache = {}
    return _memory_cache


def _save():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(_memory_cache, f, ensure_ascii=False, indent=2)


def get_cached_image_url(name, kind="creature"):
    """Le do cache sem nunca ir pra rede - retorna None se ainda nao resolvido."""
    cache = _load()
    return cache.get(f"{kind}:{name}")


def get_image_url(name, kind="creature"):
    """Retorna a URL (resolvendo e salvando no cache se for a primeira vez).
    Usar so em scripts de preparo/warm-up, nunca direto numa view."""
    with _lock:
        cache = _load()
        key = f"{kind}:{name}"
        if key in cache:
            return cache[key]
        url = wiki_images.resolve_image(name, kind)
        cache[key] = url
        _save()
        return url


def warm_cache(names, kind="creature", progress=None):
    """Resolve e cacheia uma lista de nomes de uma vez (script de preparo)."""
    with _lock:
        cache = _load()
        for i, name in enumerate(names):
            key = f"{kind}:{name}"
            if key not in cache:
                cache[key] = wiki_images.resolve_image(name, kind)
            if progress:
                progress(i, len(names))
        _save()
