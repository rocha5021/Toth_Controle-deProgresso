"""
Aba Equipamentos: lista editavel de equipamentos-alvo por personagem
(prioridade, nome, valor em kk), com adicionar/editar/excluir/duplicar/mover.
"""
import uuid

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
)


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


class EquipamentosView(QWidget):
    def __init__(self, storage_module):
        super().__init__()
        self.storage = storage_module
        self.character_config = None
        self.state = None
        self._rendering = False

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignTop)

        header_row = QHBoxLayout()
        title = QLabel("Equipamentos")
        title.setObjectName("SectionTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        add_btn = QPushButton("+ Adicionar Equipamento")
        add_btn.setObjectName("PrimaryButton")
        add_btn.clicked.connect(self._add_item)
        header_row.addWidget(add_btn)
        root.addLayout(header_row)

        sub = QLabel("Lista de equipamentos-alvo, em ordem de prioridade de compra. "
                     "Clique duas vezes numa celula pra editar nome ou valor.")
        sub.setObjectName("SectionSub")
        sub.setWordWrap(True)
        root.addWidget(sub)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["#", "Equipamento", "Valor", "Mover", "Ações"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed
        )
        self.table.itemChanged.connect(self._on_item_changed)
        root.addWidget(self.table)

    def set_character(self, character_config):
        self.character_config = character_config
        self.state = self.storage.load_character_state(character_config["id"])
        self._render()

    def _save(self):
        self.storage.save_character_state(self.character_config["id"], self.state)

    def _items(self):
        return self.state.setdefault("equipamentos", [])

    def _add_item(self):
        self._items().append({"id": uuid.uuid4().hex, "prioridade": 0, "nome": "Novo item", "valor_kk": None})
        self._save()
        self._render()

    def _duplicate(self, item_id):
        items = self._items()
        original = next(i for i in items if i["id"] == item_id)
        idx = items.index(original)
        copy = dict(original)
        copy["id"] = uuid.uuid4().hex
        copy["nome"] = original["nome"] + " (cópia)"
        items.insert(idx + 1, copy)
        self._save()
        self._render()

    def _delete(self, item_id):
        items = self._items()
        self.state["equipamentos"] = [i for i in items if i["id"] != item_id]
        self._save()
        self._render()

    def _move(self, item_id, direction):
        items = self._items()
        idx = next(i for i, it in enumerate(items) if it["id"] == item_id)
        new_idx = idx + direction
        if 0 <= new_idx < len(items):
            items[idx], items[new_idx] = items[new_idx], items[idx]
            self._save()
            self._render()

    def _on_item_changed(self, table_item):
        if self._rendering:
            return
        row = table_item.row()
        col = table_item.column()
        items = self._items()
        if row >= len(items):
            return
        entry = items[row]
        if col == 1:
            entry["nome"] = table_item.text().strip() or entry["nome"]
        elif col == 2:
            entry["valor_kk"] = _parse_valor(table_item.text())
            table_item.setText(_fmt_valor(entry["valor_kk"]))
        self._save()

    def _render(self):
        if not self.character_config:
            return
        self._rendering = True
        items = self._items()
        self.table.setRowCount(len(items))

        for row, entry in enumerate(items):
            entry["prioridade"] = row + 1

            prio_item = QTableWidgetItem(str(row + 1))
            prio_item.setFlags(prio_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, prio_item)

            self.table.setItem(row, 1, QTableWidgetItem(entry["nome"]))
            self.table.setItem(row, 2, QTableWidgetItem(_fmt_valor(entry.get("valor_kk"))))

            move_wrap = QWidget()
            move_layout = QHBoxLayout(move_wrap)
            move_layout.setContentsMargins(0, 0, 0, 0)
            up_btn = QPushButton("↑")
            up_btn.setFixedWidth(28)
            up_btn.clicked.connect(lambda _c, eid=entry["id"]: self._move(eid, -1))
            down_btn = QPushButton("↓")
            down_btn.setFixedWidth(28)
            down_btn.clicked.connect(lambda _c, eid=entry["id"]: self._move(eid, 1))
            move_layout.addWidget(up_btn)
            move_layout.addWidget(down_btn)
            self.table.setCellWidget(row, 3, move_wrap)

            actions_wrap = QWidget()
            actions_layout = QHBoxLayout(actions_wrap)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            dup_btn = QPushButton("Duplicar")
            dup_btn.clicked.connect(lambda _c, eid=entry["id"]: self._duplicate(eid))
            del_btn = QPushButton("Excluir")
            del_btn.setObjectName("DangerButton")
            del_btn.clicked.connect(lambda _c, eid=entry["id"]: self._delete(eid))
            actions_layout.addWidget(dup_btn)
            actions_layout.addWidget(del_btn)
            self.table.setCellWidget(row, 4, actions_wrap)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._rendering = False
