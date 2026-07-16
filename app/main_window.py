"""
Janela principal do Thoth: seletor de personagem (dinamico - qualquer
personagem cadastrado no banco) no topo, sidebar de navegacao, area de
conteudo com uma view por secao. Trocar de personagem re-renderiza a
secao atual com o contexto do personagem escolhido.
"""
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QButtonGroup, QFrame,
)

from db.seed import run_seed_if_needed
from controllers import character_controller
from services.background_refresh import BackgroundRefreshManager
from app.image_loader import load_pixmap
from app.views.personagem_view import PersonagemView
from app.views.bosses_view import BossesView
from app.views.charms_view import CharmsView
from app.views.bestiary_view import BestiaryView
from app.views.planejamento_view import PlanejamentoView
from app.views.novo_personagem_dialog import NovoPersonagemDialog
from app.views.news_view import NewsView
from app.views.placeholder_view import PlaceholderView

NAV_SECTIONS = [
    ("personagem", "Personagem"),
    ("planejamento", "Planejamento Estratégico"),
    ("hunts", "Hunts (Lucro)"),
    ("bosses", "Bosses"),
    ("bestiary", "Bestiary"),
    ("charms", "Charms"),
    ("quests", "Quests"),
    ("news", "Mural de Notícias"),
]

# secoes que ainda nao tem view real - mostram um aviso "em construcao"
PLACEHOLDER_DESCRIPTIONS = {
    "hunts": "Sugestao de hunts priorizando lucro liquido com o menor gasto possivel (EK) "
             "ou progresso de Bestiary (MS). Depende de um motor de custo/lucro novo — ver CHECKLIST.md.",
    "quests": "Tracker de quests concluidas/pendentes por personagem. Ainda nao recebi nenhuma lista de "
              "quests — quando voce mandar (Haxta e Tio Musga), eu populo esta tela com o progresso real.",
}

# secoes que ja tem uma view funcional propria (nao usam PlaceholderView)
REAL_VIEW_KEYS = {"personagem", "bosses", "charms", "bestiary", "planejamento", "news"}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thoth — Gerenciamento de Personagens Tibia")
        self.resize(1320, 880)

        run_seed_if_needed()
        self.characters = character_controller.list_characters()
        self.refresh_manager = BackgroundRefreshManager(
            character_names=[c["name"] for c in self.characters]
        )

        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.char_switch_bar = QFrame()
        self.char_switch_bar.setObjectName("CharacterSwitch")
        self.char_switch_bar.setStyleSheet("margin: 14px 16px 0 16px;")
        self.char_switch_layout = QHBoxLayout(self.char_switch_bar)
        self.char_switch_layout.setContentsMargins(10, 10, 10, 10)
        self.char_switch_layout.setSpacing(8)
        outer.addWidget(self.char_switch_bar)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        outer.addLayout(body)

        body.addWidget(self._build_sidebar())

        self.stack = QStackedWidget()
        body.addWidget(self.stack, stretch=1)

        self._section_views = {}
        self.personagem_view = PersonagemView(self.refresh_manager)
        self._add_section("personagem", self.personagem_view)

        self.bosses_view = BossesView()
        self._add_section("bosses", self.bosses_view)

        self.charms_view = CharmsView()
        self._add_section("charms", self.charms_view)

        self.bestiary_view = BestiaryView()
        self._add_section("bestiary", self.bestiary_view)

        self.planejamento_view = PlanejamentoView(self.refresh_manager)
        self._add_section("planejamento", self.planejamento_view)

        self.news_view = NewsView()
        self._add_section("news", self.news_view)

        for key, label in NAV_SECTIONS:
            if key in REAL_VIEW_KEYS:
                continue
            view = PlaceholderView(label, PLACEHOLDER_DESCRIPTIONS.get(key, ""))
            self._add_section(key, view)

        self._rebuild_character_switch()
        self.current_character = self.characters[0]
        self._select_character(self.current_character["id"])
        self._show_section("personagem")
        self.refresh_manager.refresh()

    def _add_section(self, key, widget):
        self._section_views[key] = widget
        self.stack.addWidget(widget)

    def _rebuild_character_switch(self):
        while self.char_switch_layout.count():
            item = self.char_switch_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        brand = QLabel("THOTH")
        brand.setStyleSheet("font-weight: 700; letter-spacing: 1px; margin-right: 12px;")
        self.char_switch_layout.addWidget(brand)

        self.char_button_group = QButtonGroup(self)
        self.char_button_group.setExclusive(True)
        for character in self.characters:
            btn = QPushButton(character["label"])
            btn.setObjectName("CharButton")
            btn.setCheckable(True)
            pixmap = load_pixmap(character.get("outfit_image_url"), 32)
            if pixmap:
                btn.setIcon(QIcon(pixmap))
                btn.setIconSize(QSize(32, 32))
            btn.clicked.connect(lambda _checked, cid=character["id"]: self._select_character(cid))
            self.char_button_group.addButton(btn)
            self.char_switch_layout.addWidget(btn)
            current_id = getattr(self, "current_character", None) and self.current_character["id"]
            target_id = current_id or self.characters[0]["id"]
            if character["id"] == target_id:
                btn.setChecked(True)

        self.char_switch_layout.addStretch()

        new_char_btn = QPushButton("+ Novo Personagem")
        new_char_btn.setObjectName("CharButton")
        new_char_btn.clicked.connect(self._open_novo_personagem)
        self.char_switch_layout.addWidget(new_char_btn)

    def _open_novo_personagem(self):
        dialog = NovoPersonagemDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            character_id = character_controller.create_character(**data)
            self.characters = character_controller.list_characters()
            self.refresh_manager.character_names = [c["name"] for c in self.characters]
            self._rebuild_character_switch()
            self._select_character(character_id)

    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(230)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 16, 10, 16)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignTop)

        self.nav_button_group = QButtonGroup(self)
        self.nav_button_group.setExclusive(True)
        for key, label in NAV_SECTIONS:
            btn = QPushButton(label)
            btn.setObjectName("NavButton")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _checked, k=key: self._show_section(k))
            self.nav_button_group.addButton(btn)
            layout.addWidget(btn)
            if key == "personagem":
                btn.setChecked(True)

        layout.addStretch()
        return sidebar

    def _select_character(self, character_id):
        self.current_character = next(c for c in self.characters if c["id"] == character_id)
        self.personagem_view.set_character(self.current_character)
        self.bosses_view.set_character(self.current_character)
        self.charms_view.set_character(self.current_character)
        self.bestiary_view.set_character(self.current_character)
        self.planejamento_view.set_character(self.current_character)

    def _show_section(self, key):
        self.stack.setCurrentWidget(self._section_views[key])
