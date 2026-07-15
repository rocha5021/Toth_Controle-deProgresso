"""
Aba Charms: banco de charms com imagem real, e selecao de "ativos"
por personagem (checkbox marcando quais estao equipados hoje).
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QCheckBox, QHBoxLayout,
)

from controllers import charms_controller
from app.image_loader import load_pixmap, prefetch_many


class CharmsView(QWidget):
    def __init__(self):
        super().__init__()
        self.character_id = None

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
        self.character_id = character_config["id"]
        charms = charms_controller.list_charms(self.character_id)
        prefetch_many([c["image_url"] for c in charms])
        self._render()

    def _toggle_active(self, name, checked):
        charms_controller.set_active(self.character_id, name, checked)

    def _render(self):
        if not self.character_id:
            return
        charms = charms_controller.list_charms(self.character_id)
        self.table.setRowCount(len(charms))

        for row, charm in enumerate(charms):
            name = charm["nome"]

            img_label = QLabel()
            pixmap = load_pixmap(charm.get("image_url"), 24)
            if pixmap:
                img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 0, img_label)

            checkbox_wrap = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_wrap)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox = QCheckBox()
            checkbox.setChecked(charm["ativo"])
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
