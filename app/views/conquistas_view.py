"""
Aba Conquistas: Titles, Achievements e Imbuements desbloqueados por
personagem - listas simples de referencia, importadas do Cyclopedia.
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTabWidget, QListWidget,
)

from controllers import conquistas_controller


class _SimpleListTab(QWidget):
    def __init__(self, loader):
        super().__init__()
        self.loader = loader
        self.character_id = None
        self._all_items = []

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)

        header = QHBoxLayout()
        self.count_label = QLabel("")
        self.count_label.setObjectName("Muted")
        header.addWidget(self.count_label)
        header.addStretch()
        root.addLayout(header)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar...")
        self.search_input.textChanged.connect(self._render)
        root.addWidget(self.search_input)

        self.list_widget = QListWidget()
        root.addWidget(self.list_widget)

    def set_character(self, character_id):
        self.character_id = character_id
        self._all_items = self.loader(character_id)
        self._render()

    def _render(self):
        search = self.search_input.text().strip().lower()
        items = [i for i in self._all_items if search in i.lower()] if search else self._all_items
        self.count_label.setText(f"{len(items)} de {len(self._all_items)} desbloqueados")
        self.list_widget.clear()
        self.list_widget.addItems(items)


class ConquistasView(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        header = QVBoxLayout()
        header.setContentsMargins(28, 24, 28, 0)
        title = QLabel("Conquistas")
        title.setObjectName("SectionTitle")
        header.addWidget(title)
        sub = QLabel("Titles, Achievements e Imbuements desbloqueados — importados do Cyclopedia do personagem.")
        sub.setObjectName("SectionSub")
        header.addWidget(sub)
        root.addLayout(header)

        self.tabs = QTabWidget()
        self.titles_tab = _SimpleListTab(conquistas_controller.list_titles)
        self.achievements_tab = _SimpleListTab(conquistas_controller.list_achievements)
        self.imbuements_tab = _SimpleListTab(conquistas_controller.list_imbuements)
        self.tabs.addTab(self.titles_tab, "Titles")
        self.tabs.addTab(self.achievements_tab, "Achievements")
        self.tabs.addTab(self.imbuements_tab, "Imbuements")
        root.addWidget(self.tabs)

    def set_character(self, character_config):
        character_id = character_config["id"]
        self.titles_tab.set_character(character_id)
        self.achievements_tab.set_character(character_id)
        self.imbuements_tab.set_character(character_id)
