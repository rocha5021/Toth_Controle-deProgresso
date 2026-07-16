"""
Atualizacao automatica dos dados reais do Tibia (personagens acompanhados
+ top 3 levels do jogo), a cada 3 horas, rodando em background (QThread)
para nao travar a interface. Tambem oferece refresh manual com um
intervalo minimo de seguranca (nao martelar a TibiaData API).
"""
import time

from PySide6.QtCore import QObject, QThread, QTimer, Signal

from services import tibiadata, storage

REFRESH_INTERVAL_MS = 3 * 60 * 60 * 1000   # 3 horas
MIN_MANUAL_REFRESH_GAP_SECONDS = 2 * 60    # 2 min


class _FetchWorker(QThread):
    finished_ok = Signal(dict)
    finished_error = Signal(str)

    def __init__(self, character_names):
        super().__init__()
        self.character_names = character_names

    def run(self):
        try:
            characters = []
            for name in self.character_names:
                try:
                    c = tibiadata.get_character(name)
                    if c:
                        characters.append(c)
                    else:
                        characters.append({"name": name, "error": "nao encontrado"})
                except Exception as e:
                    characters.append({"name": name, "error": str(e)})

            try:
                pool = tibiadata._fetch_highscore_pool()
                # so guarda o pool ja filtrado pras 5 vocacoes "de verdade" -
                # a tela monta Top N por vocacao/mundo a partir dele, sem
                # precisar buscar de novo pra cada combinacao de filtro
                level_pool = [e for e in pool if e["vocation"] in tibiadata.VALID_VOCATIONS]
            except Exception:
                cached = storage.load_tracked_cache() or {}
                level_pool = cached.get("level_pool", [])

            payload = {
                "updated_at": time.time(),
                "characters": characters,
                "level_pool": level_pool,
            }
            storage.save_tracked_cache(payload)
            self.finished_ok.emit(payload)
        except Exception as e:
            self.finished_error.emit(str(e))


class BackgroundRefreshManager(QObject):
    """Dispara refresh automatico a cada 3h e permite refresh manual.
    Emite `dataUpdated(dict)` sempre que novos dados reais chegam."""

    dataUpdated = Signal(dict)
    statusChanged = Signal(str)

    def __init__(self, character_names, parent=None):
        super().__init__(parent)
        self.character_names = character_names
        self._last_refresh = 0.0
        self._worker = None

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(REFRESH_INTERVAL_MS)

    def load_cached(self):
        return storage.load_tracked_cache()

    def refresh(self, force=False):
        if self._worker is not None and self._worker.isRunning():
            return
        if not force and (time.time() - self._last_refresh) < MIN_MANUAL_REFRESH_GAP_SECONDS:
            return

        self.statusChanged.emit("Buscando dados reais no tibia.com...")
        self._worker = _FetchWorker(self.character_names)
        self._worker.finished_ok.connect(self._on_success)
        self._worker.finished_error.connect(self._on_error)
        self._worker.start()

    def _on_success(self, payload):
        self._last_refresh = time.time()
        self.statusChanged.emit("")
        self.dataUpdated.emit(payload)

    def _on_error(self, message):
        self.statusChanged.emit(f"Erro ao atualizar: {message}")
