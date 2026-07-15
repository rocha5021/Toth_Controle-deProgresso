"""Baixa e cacheia (em memoria) os icones reais linkados da TibiaWiki
para exibir como QPixmap nas tabelas do app."""
import urllib.request

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap

_PIXMAP_CACHE = {}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Thoth/1.0"


def load_pixmap(url, size=28):
    if not url:
        return None
    cache_key = (url, size)
    if cache_key in _PIXMAP_CACHE:
        return _PIXMAP_CACHE[cache_key]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(QSize(size, size), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        _PIXMAP_CACHE[cache_key] = pixmap
        return pixmap
    except Exception:
        _PIXMAP_CACHE[cache_key] = None
        return None
