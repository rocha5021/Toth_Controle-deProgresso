"""
Aba Bosses: roster completo do Bosstiary (315 bosses, tiers Bane/Archfoe/
Nemesis), com imagem real, progresso REAL de step/kills do Bosstiary por
personagem, e farm/cooldown estimado. Busca + filtros pra nao virar uma
lista gigante sem controle.
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)

from controllers import bosses_controller
from app.image_loader import load_pixmap, prefetch_many

STEP_OPTIONS = ["Nenhum", "Bane", "Archfoe", "Nemesis"]


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

        sub = QLabel("Roster completo do Bosstiary, com progresso real de step/kills por personagem.")
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

        self.step_filter = QComboBox()
        self.step_filter.addItems(["Todos os steps"] + STEP_OPTIONS)
        self.step_filter.currentTextChanged.connect(self._apply_filters)
        filters_row.addWidget(self.step_filter)
        root.addLayout(filters_row)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["", "Boss", "Tier", "Step", "Kills", "Cooldown farm", "Status farm", "Ação"]
        )
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
        self._reload()

    def _change_step(self, boss_name, kills, step_text):
        step = STEP_OPTIONS.index(step_text)
        bosses_controller.set_bosstiary_progress(self.character_id, boss_name, step, kills)
        self._reload(keep_filters=True)

    def _adjust_kills(self, boss_name, step, delta):
        boss = next(b for b in self._all_bosses if b["nome"] == boss_name)
        new_kills = max(0, boss["bosstiary_kills"] + delta)
        bosses_controller.set_bosstiary_progress(self.character_id, boss_name, step, new_kills)
        self._reload()

    def _reload(self, keep_filters=True):
        self._all_bosses = bosses_controller.list_bosses(self.character_id)
        self._apply_filters()

    def _apply_filters(self):
        search = self.search_input.text().strip().lower()
        tier = self.tier_filter.currentText()
        step = self.step_filter.currentText()
        rows = self._all_bosses
        if search:
            rows = [b for b in rows if search in b["nome"].lower()]
        if tier != "Todos os tiers":
            rows = [b for b in rows if b["tier"] == tier]
        if step != "Todos os steps":
            rows = [b for b in rows if b["bosstiary_step_label"] == step]
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

            step_combo = QComboBox()
            step_combo.addItems(STEP_OPTIONS)
            step_combo.setCurrentText(boss["bosstiary_step_label"])
            step_combo.currentTextChanged.connect(
                lambda text, n=name, k=boss["bosstiary_kills"]: self._change_step(n, k, text)
            )
            self.table.setCellWidget(row, 3, step_combo)

            kills_wrap = QWidget()
            kills_layout = QHBoxLayout(kills_wrap)
            kills_layout.setContentsMargins(0, 0, 0, 0)
            minus_btn = QPushButton("−")
            minus_btn.setFixedWidth(24)
            minus_btn.clicked.connect(
                lambda _c, n=name, s=boss["bosstiary_step"]: self._adjust_kills(n, s, -1)
            )
            kills_label = QLabel(str(boss["bosstiary_kills"]))
            kills_label.setAlignment(Qt.AlignCenter)
            kills_label.setFixedWidth(36)
            plus_btn = QPushButton("+")
            plus_btn.setFixedWidth(24)
            plus_btn.clicked.connect(
                lambda _c, n=name, s=boss["bosstiary_step"]: self._adjust_kills(n, s, 1)
            )
            kills_layout.addWidget(minus_btn)
            kills_layout.addWidget(kills_label)
            kills_layout.addWidget(plus_btn)
            self.table.setCellWidget(row, 4, kills_wrap)

            self.table.setItem(row, 5, QTableWidgetItem(f"{boss['cooldown_dias']}d (estimado)"))
            self.table.setItem(row, 6, QTableWidgetItem(boss["status"]))

            btn = QPushButton("Farmado hoje")
            btn.setObjectName("PrimaryButton")
            btn.clicked.connect(lambda _checked, n=name: self._mark_farmed(n))
            self.table.setCellWidget(row, 7, btn)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
