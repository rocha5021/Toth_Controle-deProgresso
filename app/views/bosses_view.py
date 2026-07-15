"""
Aba Bosses: roster completo do Bosstiary (315 bosses, tiers Bane/Archfoe/
Nemesis), com imagem real e rotacao de farm por personagem (marcar quando
farmou, ver cooldown restante). Busca + filtro por tier pra nao virar uma
lista gigante sem controle.
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)

from controllers import bosses_controller
from app.image_loader import load_pixmap, prefetch_many


class BossesView(QWidget):
    def __init__(self):
        super().__init__()
        self.character_id = None
        self._all_bosses = []

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignTop)

        header_row = QHBoxLayout()
        title = QLabel("Bosses")
        title.setObjectName("SectionTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        self.count_label = QLabel("")
        self.count_label.setObjectName("Muted")
        header_row.addWidget(self.count_label)
        root.addLayout(header_row)

        sub = QLabel("Roster completo do Bosstiary. Marque quando farmar para acompanhar o cooldown (por personagem).")
        sub.setObjectName("SectionSub")
        sub.setWordWrap(True)
        root.addWidget(sub)

        filters_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar boss por nome...")
        self.search_input.textChanged.connect(self._apply_filters)
        filters_row.addWidget(self.search_input, stretch=1)

        self.tier_filter = QComboBox()
        self.tier_filter.addItems(["Todos os tiers", "Bane", "Archfoe", "Nemesis"])
        self.tier_filter.currentTextChanged.connect(self._apply_filters)
        filters_row.addWidget(self.tier_filter)
        root.addLayout(filters_row)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["", "Boss", "Tier", "Cooldown", "Status", "Ação"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        root.addWidget(self.table)

    def set_character(self, character_config):
        self.character_id = character_config["id"]
        self._all_bosses = bosses_controller.list_bosses(self.character_id)
        prefetch_many([b["image_url"] for b in self._all_bosses])
        self._apply_filters()

    def _mark_farmed(self, boss_name):
        bosses_controller.mark_farmed(self.character_id, boss_name)
        self._all_bosses = bosses_controller.list_bosses(self.character_id)
        self._apply_filters()

    def _apply_filters(self):
        search = self.search_input.text().strip().lower()
        tier = self.tier_filter.currentText()
        rows = self._all_bosses
        if search:
            rows = [b for b in rows if search in b["nome"].lower()]
        if tier != "Todos os tiers":
            rows = [b for b in rows if b["tier"] == tier]
        self._render(rows)

    def _render(self, bosses):
        self.count_label.setText(f"{len(bosses)} de {len(self._all_bosses)} bosses")
        self.table.setRowCount(len(bosses))

        for row, boss in enumerate(bosses):
            name = boss["nome"]

            img_label = QLabel()
            pixmap = load_pixmap(boss.get("image_url"), 28)
            if pixmap:
                img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 0, img_label)

            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(boss["tier"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"{boss['cooldown_dias']} dias (estimado)"))
            self.table.setItem(row, 4, QTableWidgetItem(boss["status"]))

            btn = QPushButton("Marcar farmado hoje")
            btn.setObjectName("PrimaryButton")
            btn.clicked.connect(lambda _checked, n=name: self._mark_farmed(n))
            self.table.setCellWidget(row, 5, btn)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
