"""
Mural de Noticias: atualizacoes oficiais do Tibia (patch notes, eventos
etc), direto da TibiaData API (sem scraping, sem Cloudflare). Nao e por
personagem - e a mesma pra todo mundo.
"""
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea,
)

from services import tibiadata

CATEGORY_LABELS = {
    "development": "Atualização",
    "community": "Comunidade",
    "technical": "Técnico",
    "support": "Suporte",
    "cipsoft": "CipSoft",
}


class _NewsWorker(QThread):
    finished_ok = Signal(list)
    finished_error = Signal(str)

    def run(self):
        try:
            news = tibiadata.get_latest_news(limit=30)
            self.finished_ok.emit(news)
        except Exception as e:
            self.finished_error.emit(str(e))


class NewsView(QWidget):
    def __init__(self):
        super().__init__()
        self._worker = None
        self._loaded = False

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        header = QVBoxLayout()
        header.setContentsMargins(28, 24, 28, 0)
        header_row = QHBoxLayout()
        title = QLabel("Mural de Notícias")
        title.setObjectName("SectionTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        self.refresh_btn = QPushButton("Atualizar agora")
        self.refresh_btn.setObjectName("PrimaryButton")
        self.refresh_btn.clicked.connect(self._load)
        header_row.addWidget(self.refresh_btn)
        header.addLayout(header_row)
        sub = QLabel("Últimas atualizações oficiais do Tibia (tibia.com), via TibiaData API.")
        sub.setObjectName("SectionSub")
        header.addWidget(sub)
        self.status_label = QLabel("")
        self.status_label.setObjectName("Muted")
        header.addWidget(self.status_label)
        outer.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(28, 16, 28, 20)
        self.container_layout.setSpacing(8)
        self.container_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.container)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._loaded:
            self._load()

    def _load(self):
        if self._worker is not None and self._worker.isRunning():
            return
        self.status_label.setText("Buscando notícias no tibia.com...")
        self._worker = _NewsWorker()
        self._worker.finished_ok.connect(self._on_loaded)
        self._worker.finished_error.connect(self._on_error)
        self._worker.start()

    def _on_error(self, message):
        self.status_label.setText(f"Erro ao buscar notícias: {message}")

    def _on_loaded(self, news):
        self._loaded = True
        self.status_label.setText("")
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for item in news:
            self.container_layout.addWidget(self._build_card(item))

    def _build_card(self, item):
        card = QFrame()
        card.setObjectName("Panel")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(14, 10, 14, 10)

        text_col = QVBoxLayout()
        top_row = QHBoxLayout()
        date_label = QLabel(item.get("date") or "")
        date_label.setObjectName("Muted")
        top_row.addWidget(date_label)
        badge = QLabel(CATEGORY_LABELS.get(item.get("category"), item.get("category") or ""))
        badge.setObjectName("Badge")
        top_row.addWidget(badge)
        top_row.addStretch()
        text_col.addLayout(top_row)

        title_label = QLabel(item.get("title") or "")
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        text_col.addWidget(title_label)
        layout.addLayout(text_col, stretch=1)

        open_btn = QPushButton("Abrir")
        open_btn.clicked.connect(lambda _c, url=item.get("url"): QDesktopServices.openUrl(QUrl(url)))
        layout.addWidget(open_btn)

        return card
