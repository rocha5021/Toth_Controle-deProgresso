"""View generica usada pelas abas que ainda nao foram implementadas."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class PlaceholderView(QWidget):
    def __init__(self, title, description):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setAlignment(Qt.AlignTop)

        title_label = QLabel(title)
        title_label.setObjectName("SectionTitle")
        layout.addWidget(title_label)

        sub = QLabel(description)
        sub.setObjectName("SectionSub")
        sub.setWordWrap(True)
        layout.addWidget(sub)

        note = QLabel("🚧 Em construcao — acompanhe o progresso em CHECKLIST.md")
        note.setObjectName("Muted")
        note.setStyleSheet("margin-top: 18px;")
        layout.addWidget(note)
