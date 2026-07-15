"""
Tema visual do Thoth - QSS (equivalente ao CSS do Qt) espelhando a
paleta escuro + dourado do dashboard web anterior
(legacy_web_dashboard/EK_Management_System.css).
"""

SURFACE_PAGE = "#100d09"
SURFACE_PANEL = "#1a1a19"
SURFACE_PANEL_2 = "#221f1a"
BORDER_HAIRLINE = "rgba(255,255,255,0.10)"
BORDER_GOLD = "#8a6d1f"
BORDER_GOLD_BRIGHT = "#D4AF37"
TEXT_PRIMARY = "#F5F1E6"
TEXT_SECONDARY = "#c3c2b7"
TEXT_MUTED = "#898781"
ACCENT_GOLD = "#D4AF37"
ACCENT_GOLD_BRIGHT = "#F1DE9C"
STATUS_GOOD = "#0ca30c"
STATUS_WARNING = "#fab219"
STATUS_CRITICAL = "#d03b3b"
EK_ACCENT = "#d4af37"
MS_ACCENT = "#7ab4f2"

QSS = f"""
QMainWindow, QWidget {{
    background-color: {SURFACE_PAGE};
    color: {TEXT_PRIMARY};
    font-family: "Segoe UI", sans-serif;
    font-size: 13px;
}}

#Sidebar {{
    background-color: {SURFACE_PANEL};
    border-right: 1px solid {BORDER_HAIRLINE};
}}

#BrandTitle {{
    color: {ACCENT_GOLD_BRIGHT};
    font-size: 16px;
    font-weight: 700;
    padding: 18px 14px 4px 14px;
}}

#BrandSubtitle {{
    color: {TEXT_MUTED};
    font-size: 10.5px;
    padding: 0 14px 14px 14px;
}}

QPushButton#NavButton {{
    text-align: left;
    padding: 9px 14px;
    border: none;
    border-radius: 6px;
    color: {TEXT_SECONDARY};
    background: transparent;
    font-size: 13px;
}}
QPushButton#NavButton:hover {{
    background-color: {SURFACE_PANEL_2};
    color: {TEXT_PRIMARY};
}}
QPushButton#NavButton:checked {{
    background-color: rgba(212,175,55,0.12);
    color: {ACCENT_GOLD_BRIGHT};
    font-weight: 600;
    border: 1px solid {BORDER_GOLD};
}}

#CharacterSwitch {{
    background-color: {SURFACE_PANEL};
    border: 1px solid {BORDER_HAIRLINE};
    border-radius: 8px;
}}
QPushButton#CharButton {{
    padding: 8px 18px;
    border: 1px solid transparent;
    border-radius: 6px;
    color: {TEXT_SECONDARY};
    background: transparent;
    font-weight: 600;
}}
QPushButton#CharButton:checked {{
    background-color: rgba(212,175,55,0.14);
    border: 1px solid {BORDER_GOLD_BRIGHT};
    color: {ACCENT_GOLD_BRIGHT};
}}

QFrame#Panel {{
    background-color: {SURFACE_PANEL};
    border: 1px solid {BORDER_HAIRLINE};
    border-radius: 10px;
}}
QFrame#PanelGold {{
    background-color: {SURFACE_PANEL};
    border: 1px solid {BORDER_GOLD};
    border-radius: 10px;
}}

QLabel#SectionTitle {{
    font-size: 20px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
}}
QLabel#SectionSub {{
    color: {TEXT_MUTED};
    font-size: 12px;
}}
QLabel#PanelHeader {{
    color: {ACCENT_GOLD_BRIGHT};
    font-weight: 700;
    font-size: 12.5px;
    text-transform: uppercase;
}}
QLabel#KpiValue {{
    color: {TEXT_PRIMARY};
    font-size: 22px;
    font-weight: 700;
}}
QLabel#KpiLabel {{
    color: {TEXT_MUTED};
    font-size: 10.5px;
    text-transform: uppercase;
}}
QLabel#Muted {{
    color: {TEXT_MUTED};
    font-size: 11px;
}}
QLabel#Badge {{
    background-color: rgba(212,175,55,0.10);
    color: {ACCENT_GOLD_BRIGHT};
    border: 1px solid {BORDER_GOLD};
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 10.5px;
    font-weight: 700;
}}

QPushButton#PrimaryButton {{
    background-color: {ACCENT_GOLD};
    color: #1a1408;
    border: none;
    border-radius: 6px;
    padding: 7px 14px;
    font-weight: 700;
}}
QPushButton#PrimaryButton:hover {{
    background-color: {ACCENT_GOLD_BRIGHT};
}}
QPushButton#PrimaryButton:disabled {{
    background-color: {SURFACE_PANEL_2};
    color: {TEXT_MUTED};
}}

QScrollArea {{ border: none; }}

QScrollBar:vertical {{
    background: {SURFACE_PAGE};
    width: 10px;
}}
QScrollBar::handle:vertical {{
    background: {SURFACE_PANEL_2};
    border-radius: 5px;
    min-height: 24px;
}}
"""
