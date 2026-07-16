"""
Aba Quests: quest lines concluidas por personagem. Comeca com o que o
usuario ja informou (import real do Cyclopedia) e pode ser editada.
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)

from controllers import quests_controller


class QuestsView(QWidget):
    def __init__(self):
        super().__init__()
        self.character_id = None

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignTop)

        header_row = QHBoxLayout()
        title = QLabel("Quests")
        title.setObjectName("SectionTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        self.count_label = QLabel("")
        self.count_label.setObjectName("Muted")
        header_row.addWidget(self.count_label)
        root.addLayout(header_row)

        sub = QLabel("Quest lines concluídas pelo personagem atual.")
        sub.setObjectName("SectionSub")
        root.addWidget(sub)

        add_row = QHBoxLayout()
        self.new_quest_input = QLineEdit()
        self.new_quest_input.setPlaceholderText("Nome da quest line concluída...")
        add_row.addWidget(self.new_quest_input, stretch=1)
        add_btn = QPushButton("+ Marcar como concluída")
        add_btn.setObjectName("PrimaryButton")
        add_btn.clicked.connect(self._add_quest)
        add_row.addWidget(add_btn)
        root.addLayout(add_row)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar quest...")
        self.search_input.textChanged.connect(self._render)
        root.addWidget(self.search_input)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Quest Line", "Concluída em", "Ações"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        root.addWidget(self.table)

    def set_character(self, character_config):
        self.character_id = character_config["id"]
        self._render()

    def _add_quest(self):
        name = self.new_quest_input.text().strip()
        if not name:
            return
        quests_controller.add_quest(self.character_id, name)
        self.new_quest_input.clear()
        self._render()

    def _remove_quest(self, name):
        quests_controller.remove_quest(self.character_id, name)
        self._render()

    def _render(self):
        if not self.character_id:
            return
        quests = quests_controller.list_quests(self.character_id)
        search = self.search_input.text().strip().lower()
        if search:
            quests = [q for q in quests if search in q["nome"].lower()]

        self.count_label.setText(f"{len(quests)} quest lines concluídas")
        self.table.setRowCount(len(quests))
        for row, quest in enumerate(quests):
            self.table.setItem(row, 0, QTableWidgetItem(quest["nome"]))
            self.table.setItem(row, 1, QTableWidgetItem(quest.get("completed_at") or "—"))
            del_btn = QPushButton("Remover")
            del_btn.setObjectName("DangerButton")
            del_btn.clicked.connect(lambda _c, n=quest["nome"]: self._remove_quest(n))
            self.table.setCellWidget(row, 2, del_btn)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
