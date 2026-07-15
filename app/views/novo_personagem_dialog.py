"""
Modal "Novo Personagem" - 5 perguntas obrigatorias pra cadastrar um
personagem novo com roadmap/equipamentos/metas vazios, prontos pra
preencher.
"""
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox,
    QDialogButtonBox, QLabel, QMessageBox,
)

VOCACOES = ["Elite Knight", "Royal Paladin", "Master Sorcerer", "Elder Druid", "Outro"]
FOCOS = ["Lucro", "XP", "Bestiary", "PvP/GvG", "Outro"]


class NovoPersonagemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Personagem")
        self.setMinimumWidth(400)

        form = QFormLayout(self)

        note = QLabel("Todos os campos são obrigatórios.")
        note.setObjectName("Muted")
        form.addRow(note)

        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome real do personagem no Tibia")
        form.addRow("Nome do personagem", self.nome)

        self.vocacao = QComboBox()
        self.vocacao.addItems(VOCACOES)
        form.addRow("Vocação", self.vocacao)

        self.servidor = QLineEdit()
        self.servidor.setPlaceholderText("Ex: Peloria")
        form.addRow("Servidor atual", self.servidor)

        self.level = QSpinBox()
        self.level.setRange(1, 3000)
        self.level.setValue(100)
        form.addRow("Level atual", self.level)

        self.foco = QComboBox()
        self.foco.addItems(FOCOS)
        form.addRow("Foco principal", self.foco)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def _validate_and_accept(self):
        if not self.nome.text().strip():
            QMessageBox.warning(self, "Campo obrigatório", "Informe o nome do personagem.")
            return
        if not self.servidor.text().strip():
            QMessageBox.warning(self, "Campo obrigatório", "Informe o servidor atual.")
            return
        self.accept()

    def get_data(self):
        return {
            "name": self.nome.text().strip(),
            "vocation_hint": self.vocacao.currentText(),
            "servidor": self.servidor.text().strip(),
            "level": self.level.value(),
            "focus": self.foco.currentText(),
        }
