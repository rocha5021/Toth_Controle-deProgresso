"""
Aba Charms: banco de charms com imagem real, e selecao de "ativos"
por personagem (checkbox marcando quais estao equipados hoje).
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QCheckBox, QHBoxLayout,
)

from services import reference_data, image_cache
from app.image_loader import load_pixmap

STATUS_BADGE = {
    "Ativo": "good",
    "Concluido": "good",
    "Planejado": "warning",
    "Opcional": "neutral",
}


class CharmsView(QWidget):
    def __init__(self, storage_module):
        super().__init__()
        self.storage = storage_module
        self.character_config = None
        self.state = None

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignTop)

        title = QLabel("Charms")
        title.setObjectName("SectionTitle")
        root.addWidget(title)

        sub = QLabel("Banco de charms e prioridade. Marque quais estão ativos no personagem atual.")
        sub.setObjectName("SectionSub")
        root.addWidget(sub)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["", "Ativo", "Charm", "Tipo", "Custo (CP)", "Efeito", "Status"]
        )
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        root.addWidget(self.table)

    def set_character(self, character_config):
        self.character_config = character_config
        self.state = self.storage.load_character_state(character_config["id"])
        self._render()

    def _toggle_active(self, name, checked):
        ativos = set(self.state.setdefault("charms_ativos", []))
        if checked:
            ativos.add(name)
        else:
            ativos.discard(name)
        self.state["charms_ativos"] = sorted(ativos)
        self.storage.save_character_state(self.character_config["id"], self.state)

    def _render(self):
        if not self.character_config:
            return
        charms = sorted(reference_data.CHARMS, key=lambda c: c["prioridade"])
        ativos = set((self.state or {}).get("charms_ativos", []))
        self.table.setRowCount(len(charms))

        for row, charm in enumerate(charms):
            name = charm["nome"]

            img_label = QLabel()
            url = image_cache.get_image_url(name, "charm")
            pixmap = load_pixmap(url, 24)
            if pixmap:
                img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 0, img_label)

            checkbox_wrap = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_wrap)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox = QCheckBox()
            checkbox.setChecked(name in ativos)
            checkbox.toggled.connect(lambda checked, n=name: self._toggle_active(n, checked))
            checkbox_layout.addWidget(checkbox)
            self.table.setCellWidget(row, 1, checkbox_wrap)

            self.table.setItem(row, 2, QTableWidgetItem(name))
            self.table.setItem(row, 3, QTableWidgetItem(charm["tipo"]))
            self.table.setItem(row, 4, QTableWidgetItem(str(charm["custo_cp"])))
            self.table.setItem(row, 5, QTableWidgetItem(charm["efeito"]))
            self.table.setItem(row, 6, QTableWidgetItem(charm["status"]))

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
