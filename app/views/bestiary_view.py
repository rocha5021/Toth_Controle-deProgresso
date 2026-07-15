"""
Aba Bestiary: as 645 criaturas do jogo, com imagem real, filtro por
status (Completo/Em andamento/Pendente), busca por nome e um contador
de mortes editavel por criatura (por personagem).
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QPushButton,
)

from controllers import bestiary_controller
from app.image_loader import load_pixmap, prefetch_many

STATUS_OPTIONS = ["Todos os status", "Completo", "Em andamento", "Pendente"]


class BestiaryView(QWidget):
    def __init__(self):
        super().__init__()
        self.character_id = None
        self._all_creatures = []

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignTop)

        header_row = QHBoxLayout()
        title = QLabel("Bestiary")
        title.setObjectName("SectionTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        self.count_label = QLabel("")
        self.count_label.setObjectName("Muted")
        header_row.addWidget(self.count_label)
        root.addLayout(header_row)

        sub = QLabel("Progresso de Bestiary do personagem atual — busque, filtre e registre mortes.")
        sub.setObjectName("SectionSub")
        root.addWidget(sub)

        filters_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar criatura por nome...")
        self.search_input.textChanged.connect(self._apply_filters)
        filters_row.addWidget(self.search_input, stretch=1)

        self.status_filter = QComboBox()
        self.status_filter.addItems(STATUS_OPTIONS)
        self.status_filter.currentTextChanged.connect(self._apply_filters)
        filters_row.addWidget(self.status_filter)
        root.addLayout(filters_row)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["", "Criatura", "Status", "Mortes", "Registrar"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        root.addWidget(self.table)

    def set_character(self, character_config):
        self.character_id = character_config["id"]
        self._all_creatures = bestiary_controller.list_creatures(self.character_id)
        prefetch_many([c["image_url"] for c in self._all_creatures])
        self._apply_filters()

    def _adjust_kills(self, creature_name, delta):
        creature = next(c for c in self._all_creatures if c["nome"] == creature_name)
        new_kills = max(0, creature["kills"] + delta)
        bestiary_controller.set_kills(self.character_id, creature_name, new_kills, creature["mastery_unlocked"])
        self._all_creatures = bestiary_controller.list_creatures(self.character_id)
        self._apply_filters()

    def _apply_filters(self):
        search = self.search_input.text().strip().lower()
        status = self.status_filter.currentText()
        rows = self._all_creatures
        if search:
            rows = [c for c in rows if search in c["nome"].lower()]
        if status != "Todos os status":
            rows = [c for c in rows if c["status"] == status]
        self._render(rows)

    def _render(self, creatures):
        self.count_label.setText(f"{len(creatures)} de {len(self._all_creatures)} criaturas")
        self.table.setRowCount(len(creatures))

        for row, creature in enumerate(creatures):
            name = creature["nome"]

            img_label = QLabel()
            pixmap = load_pixmap(creature.get("image_url"), 26)
            if pixmap:
                img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 0, img_label)

            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(creature["status"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(creature["kills"])))

            controls_wrap = QWidget()
            controls_layout = QHBoxLayout(controls_wrap)
            controls_layout.setContentsMargins(0, 0, 0, 0)
            minus_btn = QPushButton("−")
            minus_btn.setFixedWidth(28)
            minus_btn.clicked.connect(lambda _c, n=name: self._adjust_kills(n, -1))
            plus_btn = QPushButton("+")
            plus_btn.setFixedWidth(28)
            plus_btn.clicked.connect(lambda _c, n=name: self._adjust_kills(n, 1))
            controls_layout.addWidget(minus_btn)
            controls_layout.addWidget(plus_btn)
            self.table.setCellWidget(row, 4, controls_wrap)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
