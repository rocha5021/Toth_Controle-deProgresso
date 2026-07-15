"""
Planejamento Estrategico - substitui as antigas abas soltas Equipamentos
e Metas. 3 sub-abas simples (nao empilha tudo numa tela so):
- Ficha: resumo do personagem + etapa atual do roadmap
- Roadmap: timeline 602 -> 1000+ editavel, por etapa
- Objetivos: equipamentos (lista de compra) + metas (com modal Nova Meta)
"""
import uuid

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QFrame, QCheckBox, QLineEdit, QTextEdit, QComboBox, QDateEdit,
    QDialog, QFormLayout, QDialogButtonBox, QScrollArea,
)

from controllers import equipamentos_controller, metas_controller, roadmap_controller
from services.reference_data import PRIORIDADES_META, STATUS_META

PRIORITY_OBJECT_NAME = {
    "Muito Alta": "PriorityMuitoAlta", "Alta": "PriorityAlta",
    "Media": "PriorityMedia", "Baixa": "PriorityBaixa",
}


def _fmt_valor(valor_kk):
    if valor_kk is None or valor_kk == "":
        return ""
    return f"{valor_kk}kk"


def _parse_valor(text):
    text = text.strip().lower().replace("kk", "").replace(",", ".")
    if not text:
        return None
    try:
        val = float(text)
        return int(val) if val == int(val) else val
    except ValueError:
        return None


# ---------------------------------------------------------------- Ficha ----
class _FichaTab(QWidget):
    def __init__(self, refresh_manager):
        super().__init__()
        self.refresh_manager = refresh_manager
        self.character_config = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setAlignment(Qt.AlignTop)

        self.summary_label = QLabel("")
        self.summary_label.setObjectName("Muted")
        self.summary_label.setWordWrap(True)
        root.addWidget(self.summary_label)

        note = QLabel("Ficha completa com dados ao vivo (mortes, top level etc) fica na aba Personagem.")
        note.setObjectName("Muted")
        root.addWidget(note)

        step_header = QLabel("Etapa atual do Roadmap")
        step_header.setObjectName("PanelHeader")
        step_header.setStyleSheet("margin-top: 18px;")
        root.addWidget(step_header)

        self.step_label = QLabel("-")
        self.step_label.setObjectName("Muted")
        self.step_label.setWordWrap(True)
        root.addWidget(self.step_label)

        self.refresh_manager.dataUpdated.connect(lambda _p: self._render())

    def set_character(self, character_config):
        self.character_config = character_config
        self._render()

    def _render(self):
        if not self.character_config:
            return
        cached = self.refresh_manager.load_cached() or {}
        data = next(
            (c for c in cached.get("characters", []) if c.get("name") == self.character_config["name"]),
            None,
        )
        if data and not data.get("error"):
            self.summary_label.setText(
                f"{self.character_config['label']}  |  Level {data.get('level','-')}  |  "
                f"{data.get('vocation','-')}  |  Mundo {data.get('world','-')}  |  "
                f"Foco: {self.character_config.get('focus','-')}"
            )
        else:
            self.summary_label.setText(f"{self.character_config['label']}  |  Foco: {self.character_config.get('focus','-')}")

        steps = roadmap_controller.list_steps(self.character_config["id"])
        atual = next((s for s in steps if not s["concluido"]), steps[-1] if steps else None)
        if atual:
            fim = atual["nivel_fim"] or "1000+"
            self.step_label.setText(
                f"Level {atual['nivel_inicio']} → {fim}  ·  {atual['progresso_pct']}% preenchido  ·  "
                f"status: {atual['status']}"
            )
        else:
            self.step_label.setText("Sem etapas de roadmap cadastradas.")


# -------------------------------------------------------------- Roadmap ----
class _RoadmapStepCard(QFrame):
    def __init__(self, step, on_change):
        super().__init__()
        self.step = step
        self.on_change = on_change
        self.setObjectName("PanelGold" if not step["concluido"] else "Panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)

        header_row = QHBoxLayout()
        fim = step["nivel_fim"] or "1000+"
        title = QLabel(f"Level {step['nivel_inicio']} → {fim}")
        title.setObjectName("PanelHeader")
        header_row.addWidget(title)
        header_row.addStretch()
        self.progress_label = QLabel(f"{step['progresso_pct']}%")
        self.progress_label.setObjectName("Muted")
        header_row.addWidget(self.progress_label)
        self.concluido_check = QCheckBox("Concluído")
        self.concluido_check.setChecked(bool(step["concluido"]))
        self.concluido_check.toggled.connect(self._on_concluido)
        header_row.addWidget(self.concluido_check)
        layout.addLayout(header_row)

        self.fields = {}
        field_specs = [
            ("meta_financeira", "Meta financeira"), ("meta_equipamentos", "Meta de equipamentos"),
            ("meta_skill", "Meta de skill"), ("meta_bosses", "Meta de bosses"),
            ("meta_hunts", "Meta de hunts"),
        ]
        for key, label in field_specs:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setObjectName("Muted")
            lbl.setFixedWidth(140)
            edit = QLineEdit(step.get(key) or "")
            edit.editingFinished.connect(lambda k=key, e=edit: self._on_field_changed(k, e))
            row.addWidget(lbl)
            row.addWidget(edit)
            layout.addLayout(row)
            self.fields[key] = edit

    def _on_field_changed(self, key, edit):
        self.on_change(self.step["id"], {key: edit.text().strip()})

    def _on_concluido(self, checked):
        roadmap_controller.toggle_concluido(self.step["id"], checked)
        self.setObjectName("Panel" if checked else "PanelGold")
        self.style().unpolish(self)
        self.style().polish(self)
        self.on_change(self.step["id"], {}, refresh=True)


class _RoadmapTab(QWidget):
    def __init__(self):
        super().__init__()
        self.character_id = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(24, 20, 24, 20)
        self.container_layout.setSpacing(10)
        self.container_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.container)

        title = QLabel("Roadmap Level 602 → 1000+")
        title.setObjectName("SectionTitle")
        self.container_layout.addWidget(title)
        sub = QLabel("Timeline editável por etapa — preencha as metas conforme for planejando.")
        sub.setObjectName("SectionSub")
        self.container_layout.addWidget(sub)

    def set_character(self, character_config):
        self.character_id = character_config["id"]
        self._render()

    def _on_step_change(self, step_id, fields, refresh=False):
        if fields:
            roadmap_controller.update_step(step_id, fields)
        if refresh:
            self._render()

    def _render(self):
        while self.container_layout.count() > 2:
            item = self.container_layout.takeAt(2)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        steps = roadmap_controller.list_steps(self.character_id)
        for step in steps:
            card = _RoadmapStepCard(step, self._on_step_change)
            self.container_layout.addWidget(card)


# ------------------------------------------------------------ Objetivos ----
class NovaMetaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nova Meta")
        self.setMinimumWidth(420)
        form = QFormLayout(self)

        self.titulo = QLineEdit()
        form.addRow("Título", self.titulo)
        self.descricao = QTextEdit()
        self.descricao.setFixedHeight(60)
        form.addRow("Descrição", self.descricao)
        self.categoria = QComboBox()
        self.categoria.addItems([
            "Equipamento", "Hunt", "Boss", "Skill", "Charm",
            "Financeiro", "Quest", "Transferência", "Outros",
        ])
        form.addRow("Categoria", self.categoria)
        self.prioridade = QComboBox()
        self.prioridade.addItems(PRIORIDADES_META)
        form.addRow("Prioridade", self.prioridade)
        self.data = QDateEdit()
        self.data.setCalendarPopup(True)
        self.data.setDisplayFormat("dd/MM/yyyy")
        self.data.setDate(QDate.currentDate())
        form.addRow("Data", self.data)
        self.valor = QLineEdit()
        self.valor.setPlaceholderText("Ex: 55 (em kk)")
        form.addRow("Valor (kk)", self.valor)
        self.observacoes = QTextEdit()
        self.observacoes.setFixedHeight(50)
        form.addRow("Observações", self.observacoes)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def get_data(self):
        return {
            "titulo": self.titulo.text().strip() or "Sem título",
            "descricao": self.descricao.toPlainText().strip(),
            "categoria": self.categoria.currentText(),
            "prioridade": self.prioridade.currentText(),
            "deadline": self.data.date().toString("yyyy-MM-dd"),
            "valor_kk": _parse_valor(self.valor.text()),
            "observacoes": self.observacoes.toPlainText().strip(),
        }


class _ObjetivosTab(QWidget):
    def __init__(self):
        super().__init__()
        self.character_id = None
        self._rendering = False

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setAlignment(Qt.AlignTop)

        equip_header = QHBoxLayout()
        equip_title = QLabel("Equipamentos")
        equip_title.setObjectName("PanelHeader")
        equip_header.addWidget(equip_title)
        equip_header.addStretch()
        add_equip_btn = QPushButton("+ Adicionar")
        add_equip_btn.setObjectName("PrimaryButton")
        add_equip_btn.clicked.connect(self._add_equipamento)
        equip_header.addWidget(add_equip_btn)
        root.addLayout(equip_header)

        self.equip_table = QTableWidget(0, 5)
        self.equip_table.setHorizontalHeaderLabels(["#", "Equipamento", "Valor", "Mover", "Ações"])
        self.equip_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.equip_table.verticalHeader().setVisible(False)
        self.equip_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.equip_table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.equip_table.itemChanged.connect(self._on_equip_item_changed)
        self.equip_table.setMaximumHeight(280)
        root.addWidget(self.equip_table)

        metas_header = QHBoxLayout()
        metas_title = QLabel("Metas")
        metas_title.setObjectName("PanelHeader")
        metas_title.setStyleSheet("margin-top: 18px;")
        metas_header.addWidget(metas_title)
        metas_header.addStretch()
        add_meta_btn = QPushButton("+ Nova Meta")
        add_meta_btn.setObjectName("PrimaryButton")
        add_meta_btn.clicked.connect(self._open_new_meta_dialog)
        metas_header.addWidget(add_meta_btn)
        root.addLayout(metas_header)

        self.metas_table = QTableWidget(0, 6)
        self.metas_table.setHorizontalHeaderLabels(["Título", "Categoria", "Prioridade", "Valor", "Status", "Ações"])
        self.metas_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.metas_table.verticalHeader().setVisible(False)
        self.metas_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.metas_table.setSelectionMode(QAbstractItemView.NoSelection)
        root.addWidget(self.metas_table)

    def set_character(self, character_config):
        self.character_id = character_config["id"]
        self._render()

    def _render(self):
        self._render_equip()
        self._render_metas()

    # -- equipamentos --
    def _add_equipamento(self):
        equipamentos_controller.add_item(self.character_id)
        self._render_equip()

    def _render_equip(self):
        self._rendering = True
        items = equipamentos_controller.list_items(self.character_id)
        self.equip_table.setRowCount(len(items))
        for row, item in enumerate(items):
            prio_item = QTableWidgetItem(str(row + 1))
            prio_item.setFlags(prio_item.flags() & ~Qt.ItemIsEditable)
            self.equip_table.setItem(row, 0, prio_item)
            self.equip_table.setItem(row, 1, QTableWidgetItem(item["nome"]))
            self.equip_table.setItem(row, 2, QTableWidgetItem(_fmt_valor(item.get("valor_kk"))))

            move_wrap = QWidget()
            move_layout = QHBoxLayout(move_wrap)
            move_layout.setContentsMargins(0, 0, 0, 0)
            up_btn = QPushButton("↑")
            up_btn.setFixedWidth(26)
            up_btn.clicked.connect(lambda _c, iid=item["id"]: self._move_equip(iid, -1))
            down_btn = QPushButton("↓")
            down_btn.setFixedWidth(26)
            down_btn.clicked.connect(lambda _c, iid=item["id"]: self._move_equip(iid, 1))
            move_layout.addWidget(up_btn)
            move_layout.addWidget(down_btn)
            self.equip_table.setCellWidget(row, 3, move_wrap)

            actions_wrap = QWidget()
            actions_layout = QHBoxLayout(actions_wrap)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            dup_btn = QPushButton("Duplicar")
            dup_btn.clicked.connect(lambda _c, iid=item["id"]: self._duplicate_equip(iid))
            del_btn = QPushButton("Excluir")
            del_btn.setObjectName("DangerButton")
            del_btn.clicked.connect(lambda _c, iid=item["id"]: self._delete_equip(iid))
            actions_layout.addWidget(dup_btn)
            actions_layout.addWidget(del_btn)
            self.equip_table.setCellWidget(row, 4, actions_wrap)
        self.equip_table.resizeColumnsToContents()
        self.equip_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._rendering = False

    def _on_equip_item_changed(self, table_item):
        if self._rendering:
            return
        items = equipamentos_controller.list_items(self.character_id)
        row = table_item.row()
        if row >= len(items):
            return
        item_id = items[row]["id"]
        col = table_item.column()
        if col == 1:
            equipamentos_controller.update_field(item_id, "nome", table_item.text().strip())
        elif col == 2:
            valor = _parse_valor(table_item.text())
            equipamentos_controller.update_field(item_id, "valor_kk", valor)
            table_item.setText(_fmt_valor(valor))

    def _move_equip(self, item_id, direction):
        equipamentos_controller.move(self.character_id, item_id, direction)
        self._render_equip()

    def _duplicate_equip(self, item_id):
        equipamentos_controller.duplicate(self.character_id, item_id)
        self._render_equip()

    def _delete_equip(self, item_id):
        equipamentos_controller.delete(item_id)
        self._render_equip()

    # -- metas --
    def _open_new_meta_dialog(self):
        dialog = NovaMetaDialog(self)
        if dialog.exec() == QDialog.Accepted:
            metas_controller.add_goal(self.character_id, dialog.get_data())
            self._render_metas()

    def _delete_meta(self, goal_id):
        metas_controller.delete_goal(goal_id)
        self._render_metas()

    def _change_status(self, goal_id, status):
        metas_controller.set_status(goal_id, status)

    def _render_metas(self):
        goals = metas_controller.list_goals(self.character_id)
        self.metas_table.setRowCount(len(goals))
        for row, goal in enumerate(goals):
            self.metas_table.setItem(row, 0, QTableWidgetItem(goal["titulo"]))
            self.metas_table.setItem(row, 1, QTableWidgetItem(goal.get("categoria") or ""))

            prio_label = QLabel(goal["prioridade"])
            prio_label.setObjectName(PRIORITY_OBJECT_NAME.get(goal["prioridade"], "PriorityMedia"))
            prio_label.setAlignment(Qt.AlignCenter)
            self.metas_table.setCellWidget(row, 2, prio_label)

            valor_kk = goal.get("valor_kk")
            self.metas_table.setItem(row, 3, QTableWidgetItem(_fmt_valor(valor_kk)))

            status_combo = QComboBox()
            status_combo.addItems(STATUS_META)
            status_combo.setCurrentText(goal.get("status", "Pendente"))
            status_combo.currentTextChanged.connect(lambda text, gid=goal["id"]: self._change_status(gid, text))
            self.metas_table.setCellWidget(row, 4, status_combo)

            del_btn = QPushButton("Excluir")
            del_btn.setObjectName("DangerButton")
            del_btn.clicked.connect(lambda _c, gid=goal["id"]: self._delete_meta(gid))
            self.metas_table.setCellWidget(row, 5, del_btn)
        self.metas_table.resizeColumnsToContents()
        self.metas_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)


# ---------------------------------------------------------------- Root ----
class PlanejamentoView(QWidget):
    def __init__(self, refresh_manager):
        super().__init__()
        self.character_config = None

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        header = QVBoxLayout()
        header.setContentsMargins(28, 24, 28, 0)
        title = QLabel("Planejamento Estratégico")
        title.setObjectName("SectionTitle")
        header.addWidget(title)
        sub = QLabel("Evolução completa do personagem: ficha, roadmap e próximos objetivos.")
        sub.setObjectName("SectionSub")
        header.addWidget(sub)
        root.addLayout(header)

        self.tabs = QTabWidget()
        self.ficha_tab = _FichaTab(refresh_manager)
        self.roadmap_tab = _RoadmapTab()
        self.objetivos_tab = _ObjetivosTab()
        self.tabs.addTab(self.ficha_tab, "Ficha")
        self.tabs.addTab(self.roadmap_tab, "Roadmap")
        self.tabs.addTab(self.objetivos_tab, "Objetivos")
        root.addWidget(self.tabs)

    def set_character(self, character_config):
        self.character_config = character_config
        self.ficha_tab.set_character(character_config)
        self.roadmap_tab.set_character(character_config)
        self.objetivos_tab.set_character(character_config)
