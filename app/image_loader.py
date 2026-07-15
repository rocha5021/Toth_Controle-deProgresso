"""
Baixa e cacheia os icones reais linkados da TibiaWiki para exibir como
QPixmap nas tabelas do app.

Duas camadas de cache:
1. Disco (`data/image_files/`) - baixa uma vez, reusa pra sempre entre
   execucoes do app. Sem isso, toda abertura do app teria que rebaixar
   todas as imagens de novo.
2. Memoria - evita reler do disco toda vez que uma tela e re-renderizada.

`prefetch_many` baixa varias imagens em paralelo (rede e I/O bound, nao
CPU) - baixar 600+ imagens uma por uma e o motivo de listas grandes
(Bestiary, Bosses) travarem por minutos; em paralelo leva poucos segundos.
"""
import hashlib
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap

_PIXMAP_CACHE = {}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Thoth/1.0"
DISK_CACHE_DIR = Path(__file__).parent.parent / "data" / "image_files"


def _disk_path(url):
    ext = url.rsplit(".", 1)[-1][:4] if "." in url.rsplit("/", 1)[-1] else "img"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return DISK_CACHE_DIR / f"{digest}.{ext}"


def _download_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=8) as resp:
        return resp.read()


def _ensure_on_disk(url):
    """Garante que a imagem esta no disco, baixando se preciso. Retorna o path."""
    path = _disk_path(url)
    if path.exists():
        return path
    try:
        data = _download_bytes(url)
        DISK_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path
    except Exception:
        return None


def load_pixmap(url, size=28):
    if not url:
        return None
    cache_key = (url, size)
    if cache_key in _PIXMAP_CACHE:
        return _PIXMAP_CACHE[cache_key]

    path = _disk_path(url)
    if not path.exists():
        path = _ensure_on_disk(url)
    if not path:
        _PIXMAP_CACHE[cache_key] = None
        return None

    pixmap = QPixmap(str(path))
    pixmap = pixmap.scaled(QSize(size, size), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    _PIXMAP_CACHE[cache_key] = pixmap
    return pixmap


def prefetch_many(urls, max_workers=32):
    """Baixa em paralelo todas as urls que ainda nao estao em disco.
    Chamar ANTES de renderizar uma tabela grande (Bestiary/Bosses) evita
    o travamento de baixar centenas de imagens uma por uma."""
    missing = [u for u in set(urls) if u and not _disk_path(u).exists()]
    if not missing:
        return
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        list(pool.map(_ensure_on_disk, missing))
