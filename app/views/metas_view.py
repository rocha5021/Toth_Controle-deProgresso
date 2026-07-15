"""
Aba Metas: lista de metas por personagem, com modal "Nova Meta" e
prioridade colorida automaticamente (Muito Alta/Alta/Media/Baixa).
"""
import uuid

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QDialog, QFormLayout, QLineEdit, QTextEdit, QComboBox, QDateEdit,
    QDialogButtonBox,
)

from services.reference_data import PRIORIDADES_META, STATUS_META

PRIORITY_OBJECT_NAME = {
    "Muito Alta": "PriorityMuitoAlta",
    "Alta": "PriorityAlta",
    "Media": "PriorityMedia",
    "Baixa": "PriorityBaixa",
}


class NovaMetaDialog(QDialog):
    def __init__(self, parent=None, meta=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Meta" if meta else "Nova Meta")
        self.setMinimumWidth(420)

        form = QFormLayout(self)

        self.titulo = QLineEdit(meta["titulo"] if meta else "")
        form.addRow("Título", self.titulo)

        self.descricao = QTextEdit(meta["descricao"] if meta else "")
        self.descricao.setFixedHeight(70)
        form.addRow("Descrição", self.descricao)

        self.categoria = QLineEdit(meta["categoria"] if meta else "")
        form.addRow("Categoria", self.categoria)

        self.prioridade = QComboBox()
        self.prioridade.addItems(PRIORIDADES_META)
        if meta:
            self.prioridade.setCurrentText(meta["prioridade"])
        form.addRow("Prioridade", self.prioridade)

        self.data = QDateEdit()
        self.data.setCalendarPopup(True)
        self.data.setDisplayFormat("dd/MM/yyyy")
        if meta and meta.get("data"):
            self.data.setDate(QDate.fromString(meta["data"], "yyyy-MM-dd"))
        else:
            self.data.setDate(QDate.currentDate())
        form.addRow("Data", self.data)

        self.valor = QLineEdit(str(meta["valor_kk"]) if meta and meta.get("valor_kk") is not None else "")
        self.valor.setPlaceholderText("Ex: 55 (em kk)")
        form.addRow("Valor (kk)", self.valor)

        self.observacoes = QTextEdit(meta["observacoes"] if meta else "")
        self.observacoes.setFixedHeight(60)
        form.addRow("Observações", self.observacoes)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def get_data(self):
        valor_text = self.valor.text().strip().replace("kk", "").replace(",", ".")
        valor_kk = None
        if valor_text:
            try:
                valor_kk = float(valor_text)
                if valor_kk == int(valor_kk):
                    valor_kk = int(valor_kk)
            except ValueError:
                valor_kk = None
        return {
            "titulo": self.titulo.text().strip() or "Sem título",
            "descricao": self.descricao.toPlainText().strip(),
            "categoria": self.categoria.text().strip(),
            "prioridade": self.prioridade.currentText(),
            "data": self.data.date().toString("yyyy-MM-dd"),
            "valor_kk": valor_kk,
            "observacoes": self.observacoes.toPlainText().strip(),
        }


class MetasView(QWidget):
    def __init__(self, storage_module):
        super().__init__()
        self.storage = storage_module
        self.character_config = None
        self.state = None

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignTop)

        header_row = QHBoxLayout()
        title = QLabel("Metas")
        title.setObjectName("SectionTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        add_btn = QPushButton("+ Nova Meta")
        add_btn.setObjectName("PrimaryButton")
        add_btn.clicked.connect(self._open_new_meta_dialog)
        header_row.addWidget(add_btn)
        root.addLayout(header_row)

        sub = QLabel("Metas de progressão do personagem — compras, level, skills, planejamento.")
        sub.setObjectName("SectionSub")
        root.addWidget(sub)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["Título", "Categoria", "Prioridade", "Data", "Valor", "Status", "Ações"]
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        root.addWidget(self.table)

    def set_character(self, character_config):
        self.character_config = character_config
        self.state = self.storage.load_character_state(character_config["id"])
        self._render()

    def _save(self):
        self.storage.save_character_state(self.character_config["id"], self.state)

    def _metas(self):
        return self.state.setdefault("metas", [])

    def _open_new_meta_dialog(self):
        dialog = NovaMetaDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            data["id"] = uuid.uuid4().hex
            data["status"] = "Pendente"
            self._metas().append(data)
            self._save()
            self._render()

    def _edit_meta(self, meta_id):
        meta = next(m for m in self._metas() if m["id"] == meta_id)
        dialog = NovaMetaDialog(self, meta=meta)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            meta.update(data)
            self._save()
            self._render()

    def _delete_meta(self, meta_id):
        self.state["metas"] = [m for m in self._metas() if m["id"] != meta_id]
        self._save()
        self._render()

    def _change_status(self, meta_id, new_status):
        meta = next(m for m in self._metas() if m["id"] == meta_id)
        meta["status"] = new_status
        self._save()

    def _render(self):
        if not self.character_config:
            return
        metas = self._metas()
        self.table.setRowCount(len(metas))

        for row, meta in enumerate(metas):
            self.table.setItem(row, 0, QTableWidgetItem(meta["titulo"]))
            self.table.setItem(row, 1, QTableWidgetItem(meta.get("categoria", "")))

            prio_label = QLabel(meta["prioridade"])
            prio_label.setObjectName(PRIORITY_OBJECT_NAME.get(meta["prioridade"], "PriorityMedia"))
            prio_label.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 2, prio_label)

            data_str = meta.get("data", "")
            if data_str:
                try:
                    data_str = QDate.fromString(data_str, "yyyy-MM-dd").toString("dd/MM/yyyy")
                except Exception:
                    pass
            self.table.setItem(row, 3, QTableWidgetItem(data_str))

            valor_kk = meta.get("valor_kk")
            self.table.setItem(row, 4, QTableWidgetItem(f"{valor_kk}kk" if valor_kk is not None else ""))

            status_combo = QComboBox()
            status_combo.addItems(STATUS_META)
            status_combo.setCurrentText(meta.get("status", "Pendente"))
            status_combo.currentTextChanged.connect(
                lambda text, mid=meta["id"]: self._change_status(mid, text)
            )
            self.table.setCellWidget(row, 5, status_combo)

            actions_wrap = QWidget()
            actions_layout = QHBoxLayout(actions_wrap)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            edit_btn = QPushButton("Editar")
            edit_btn.clicked.connect(lambda _c, mid=meta["id"]: self._edit_meta(mid))
            del_btn = QPushButton("Excluir")
            del_btn.setObjectName("DangerButton")
            del_btn.clicked.connect(lambda _c, mid=meta["id"]: self._delete_meta(mid))
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(del_btn)
            self.table.setCellWidget(row, 6, actions_wrap)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
