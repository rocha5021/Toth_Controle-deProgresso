"""
Aba Personagem: ficha com dados reais (ao vivo) do personagem selecionado,
mais o Top 3 de level do Tibia (varredura real dos 93 mundos).
"""
from datetime import datetime, timezone

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QComboBox,
)


TODAS_VOCACOES = "Todas as vocações"


def _time_ago(epoch_seconds):
    if not epoch_seconds:
        return "-"
    diff = datetime.now(timezone.utc).timestamp() - epoch_seconds
    minutes = int(diff // 60)
    if minutes < 1:
        return "agora mesmo"
    if minutes < 60:
        return f"ha {minutes} min"
    hours = minutes // 60
    if hours < 24:
        return f"ha {hours}h{minutes % 60}min"
    return f"ha {hours // 24}d"


def _kpi(value, label):
    box = QFrame()
    box.setObjectName("Panel")
    layout = QVBoxLayout(box)
    layout.setContentsMargins(14, 10, 14, 10)
    val = QLabel(str(value))
    val.setObjectName("KpiValue")
    lbl = QLabel(label)
    lbl.setObjectName("KpiLabel")
    layout.addWidget(val)
    layout.addWidget(lbl)
    return box


class PersonagemView(QWidget):
    def __init__(self, refresh_manager):
        super().__init__()
        self.refresh_manager = refresh_manager
        self.character_config = None
        self._latest_payload = None

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setAlignment(Qt.AlignTop)

        header_row = QHBoxLayout()
        title = QLabel("Personagem")
        title.setObjectName("SectionTitle")
        header_row.addWidget(title)
        header_row.addStretch()
        self.updated_label = QLabel("-")
        self.updated_label.setObjectName("Muted")
        header_row.addWidget(self.updated_label)
        self.refresh_btn = QPushButton("Atualizar agora")
        self.refresh_btn.setObjectName("PrimaryButton")
        self.refresh_btn.clicked.connect(lambda: self.refresh_manager.refresh(force=True))
        header_row.addWidget(self.refresh_btn)
        root.addLayout(header_row)

        self.status_label = QLabel("")
        self.status_label.setObjectName("Muted")
        root.addWidget(self.status_label)

        self.kpi_row = QGridLayout()
        self.kpi_row.setSpacing(10)
        root.addLayout(self.kpi_row)

        self.info_label = QLabel("")
        self.info_label.setObjectName("Muted")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("margin-top: 10px;")
        root.addWidget(self.info_label)

        deaths_header = QLabel("Mortes recentes")
        deaths_header.setObjectName("PanelHeader")
        deaths_header.setStyleSheet("margin-top: 18px;")
        root.addWidget(deaths_header)
        self.deaths_label = QLabel("-")
        self.deaths_label.setObjectName("Muted")
        self.deaths_label.setWordWrap(True)
        root.addWidget(self.deaths_label)

        top_header_row = QHBoxLayout()
        top_header_row.setContentsMargins(0, 22, 0, 0)
        top_header = QLabel("Top 20 Level do Tibia (todos os servidores)")
        top_header.setObjectName("PanelHeader")
        top_header_row.addWidget(top_header)
        top_header_row.addStretch()
        self.vocation_filter = QComboBox()
        self.vocation_filter.addItem(TODAS_VOCACOES)
        self.vocation_filter.currentTextChanged.connect(self._render_top_table)
        top_header_row.addWidget(self.vocation_filter)
        root.addLayout(top_header_row)

        self.top_table = QTableWidget(0, 4)
        self.top_table.setHorizontalHeaderLabels(["Personagem", "Level", "Vocacao", "Mundo"])
        self.top_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.top_table.verticalHeader().setVisible(False)
        self.top_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.top_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.top_table.setMaximumHeight(420)
        root.addWidget(self.top_table)

        root.addStretch()

        self.refresh_manager.dataUpdated.connect(self._on_data_updated)
        self.refresh_manager.statusChanged.connect(self._on_status_changed)

        cached = self.refresh_manager.load_cached()
        if cached:
            self._latest_payload = cached
            self._render()

    def set_character(self, character_config):
        self.character_config = character_config
        self._render()

    def _on_status_changed(self, message):
        self.status_label.setText(message)

    def _on_data_updated(self, payload):
        self._latest_payload = payload
        self._render()

    def _clear_kpis(self):
        while self.kpi_row.count():
            item = self.kpi_row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _render(self):
        self._clear_kpis()
        if not self.character_config or not self._latest_payload:
            return

        char_name = self.character_config["name"]
        data = next(
            (c for c in self._latest_payload.get("characters", []) if c.get("name") == char_name),
            None,
        )

        if not data or data.get("error"):
            err = data.get("error") if data else "sem dados ainda"
            self.info_label.setText(f"Nao foi possivel carregar {char_name}: {err}")
        else:
            kpis = [
                (data.get("level", "-"), "Level"),
                (data.get("world", "-"), "Mundo"),
                (data.get("vocation", "-"), "Vocacao"),
                (data.get("achievement_points", "-"), "Achievement Points"),
            ]
            for i, (value, label) in enumerate(kpis):
                self.kpi_row.addWidget(_kpi(value, label), 0, i)

            self.info_label.setText(
                f"Residencia: {data.get('residence', '-')}  |  "
                f"Guild: {data.get('guild') or '-'}  |  "
                f"{data.get('account_status', '')}  |  "
                f"Ultimo login: {data.get('last_login', '-')}"
            )

            deaths = data.get("deaths") or []
            if deaths:
                lines = [f"Level {d['level']} - {d['reason']}" for d in deaths[:3]]
                self.deaths_label.setText("\n".join(lines))
            else:
                self.deaths_label.setText("Sem mortes recentes.")

        updated_at = self._latest_payload.get("updated_at")
        self.updated_label.setText(f"Atualizado {_time_ago(updated_at)}")

        by_vocation = self._latest_payload.get("top_levels_by_vocation", {})
        current_selection = self.vocation_filter.currentText()
        self.vocation_filter.blockSignals(True)
        self.vocation_filter.clear()
        self.vocation_filter.addItem(TODAS_VOCACOES)
        for voc in sorted(by_vocation.keys()):
            self.vocation_filter.addItem(voc)
        idx = self.vocation_filter.findText(current_selection)
        self.vocation_filter.setCurrentIndex(idx if idx >= 0 else 0)
        self.vocation_filter.blockSignals(False)

        self._render_top_table()

    def _render_top_table(self):
        if not self._latest_payload:
            return
        selection = self.vocation_filter.currentText()
        if selection and selection != TODAS_VOCACOES:
            top_levels = self._latest_payload.get("top_levels_by_vocation", {}).get(selection, [])
        else:
            top_levels = self._latest_payload.get("top_levels", [])

        self.top_table.setRowCount(len(top_levels))
        for row, entry in enumerate(top_levels):
            self.top_table.setItem(row, 0, QTableWidgetItem(entry.get("name", "-")))
            self.top_table.setItem(row, 1, QTableWidgetItem(str(entry.get("level", "-"))))
            self.top_table.setItem(row, 2, QTableWidgetItem(entry.get("vocation", "-")))
            self.top_table.setItem(row, 3, QTableWidgetItem(entry.get("world", "-")))
