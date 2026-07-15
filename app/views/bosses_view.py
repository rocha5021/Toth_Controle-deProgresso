"""
Aba Bosses: banco de bosses com imagem real, e rotacao de farm por
personagem (marcar quando farmou, ver cooldown restante).
"""
from datetime import datetime, timezone

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)

from services import reference_data, image_cache
from app.image_loader import load_pixmap


def _today_iso():
    return datetime.now(timezone.utc).date().isoformat()


def _days_since(iso_date):
    if not iso_date:
        return None
    then = datetime.fromisoformat(iso_date).date()
    return (datetime.now(timezone.utc).date() - then).days


class BossesView(QWidget):
    def __init__(self, storage_module):
        super().__init__()
        self.storage = storage_module
        self.character_config = None
        self.state = None

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignTop)

        title = QLabel("Bosses — Rotação")
        title.setObjectName("SectionTitle")
        root.addWidget(title)

        sub = QLabel("Marque quando farmar para acompanhar o cooldown de cada boss (por personagem).")
        sub.setObjectName("SectionSub")
        root.addWidget(sub)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["", "Boss", "Local", "Cooldown", "Status", "Ação"]
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        root.addWidget(self.table)

    def set_character(self, character_config):
        self.character_config = character_config
        self.state = self.storage.load_character_state(character_config["id"])
        self._render()

    def _mark_farmed(self, boss_name):
        self.state.setdefault("boss_farm_log", {})[boss_name] = _today_iso()
        self.storage.save_character_state(self.character_config["id"], self.state)
        self._render()

    def _render(self):
        if not self.character_config:
            return
        bosses = reference_data.BOSSES
        self.table.setRowCount(len(bosses))
        farm_log = (self.state or {}).get("boss_farm_log", {})

        for row, boss in enumerate(bosses):
            name = boss["nome"]

            img_label = QLabel()
            url = image_cache.get_image_url(name, "creature")
            pixmap = load_pixmap(url, 28)
            if pixmap:
                img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 0, img_label)

            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(boss["local"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"{boss['cooldown_dias']} dias"))

            last_farmed = farm_log.get(name)
            days = _days_since(last_farmed)
            if days is None:
                status_text = "Nunca farmado"
            elif days >= boss["cooldown_dias"]:
                status_text = "Disponível"
            else:
                status_text = f"Aguardar {boss['cooldown_dias'] - days}d"
            self.table.setItem(row, 4, QTableWidgetItem(status_text))

            btn = QPushButton("Marcar farmado hoje")
            btn.setObjectName("PrimaryButton")
            btn.clicked.connect(lambda _checked, n=name: self._mark_farmed(n))
            self.table.setCellWidget(row, 5, btn)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
