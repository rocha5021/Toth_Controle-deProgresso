"""Thoth - ponto de entrada do app desktop."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.theme import QSS

ICON_PATH = Path(__file__).parent / "app" / "thoth_icon.ico"


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    app.setWindowIcon(QIcon(str(ICON_PATH)))
    window = MainWindow()
    window.setWindowIcon(QIcon(str(ICON_PATH)))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
