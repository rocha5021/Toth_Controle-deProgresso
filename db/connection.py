"""
Camada Model/DB do Thoth - SQLite (biblioteca padrao do Python, sem
dependencia nova). Um unico arquivo `data/thoth.db` guarda tudo:
personagens, equipamentos, metas, roadmap, progresso de bestiary,
farm de bosses e charms ativos - tudo separado por character_id.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "thoth.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS characters (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    label TEXT,
    vocation_hint TEXT,
    focus TEXT,
    accent_color TEXT,
    outfit_image_url TEXT
);

CREATE TABLE IF NOT EXISTS equipment_planning (
    id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL,
    prioridade INTEGER,
    nome TEXT NOT NULL,
    valor_kk REAL,
    categoria TEXT,
    status TEXT,
    roi_preco REAL,
    roi_beneficio TEXT,
    roi_impacto TEXT,
    observacoes TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS goals (
    id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    categoria TEXT,
    status TEXT,
    prioridade TEXT,
    valor_kk REAL,
    deadline TEXT,
    observacoes TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS roadmap_steps (
    id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL,
    ordem INTEGER,
    nivel_inicio INTEGER,
    nivel_fim INTEGER,
    meta_financeira TEXT,
    meta_equipamentos TEXT,
    meta_skill TEXT,
    meta_bosses TEXT,
    meta_hunts TEXT,
    status TEXT,
    progresso_pct INTEGER DEFAULT 0,
    concluido INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS bestiary_progress (
    character_id TEXT NOT NULL,
    creature_name TEXT NOT NULL,
    kills INTEGER DEFAULT 0,
    mastery_unlocked INTEGER DEFAULT 0,
    PRIMARY KEY (character_id, creature_name)
);

CREATE TABLE IF NOT EXISTS boss_farm_log (
    character_id TEXT NOT NULL,
    boss_name TEXT NOT NULL,
    last_farmed_date TEXT,
    PRIMARY KEY (character_id, boss_name)
);

CREATE TABLE IF NOT EXISTS charms_active (
    character_id TEXT NOT NULL,
    charm_name TEXT NOT NULL,
    grade INTEGER,
    PRIMARY KEY (character_id, charm_name)
);

CREATE TABLE IF NOT EXISTS bosstiary_progress (
    character_id TEXT NOT NULL,
    boss_name TEXT NOT NULL,
    step INTEGER DEFAULT 0,
    kills INTEGER DEFAULT 0,
    PRIMARY KEY (character_id, boss_name)
);

CREATE TABLE IF NOT EXISTS quests_completed (
    character_id TEXT NOT NULL,
    quest_name TEXT NOT NULL,
    completed_at TEXT,
    PRIMARY KEY (character_id, quest_name)
);

CREATE TABLE IF NOT EXISTS titles_unlocked (
    character_id TEXT NOT NULL,
    title_name TEXT NOT NULL,
    PRIMARY KEY (character_id, title_name)
);

CREATE TABLE IF NOT EXISTS achievements_unlocked (
    character_id TEXT NOT NULL,
    achievement_name TEXT NOT NULL,
    PRIMARY KEY (character_id, achievement_name)
);

CREATE TABLE IF NOT EXISTS imbuements_unlocked (
    character_id TEXT NOT NULL,
    imbuement_name TEXT NOT NULL,
    PRIMARY KEY (character_id, imbuement_name)
);
"""

_connection = None


def get_connection():
    global _connection
    if _connection is None:
        DB_PATH.parent.mkdir(exist_ok=True)
        _connection = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA foreign_keys = ON")
        _connection.executescript(SCHEMA)
        _connection.commit()
    return _connection


def is_fresh_database():
    """True se o banco acabou de ser criado (nenhum personagem cadastrado)."""
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) AS c FROM characters").fetchone()
    return row["c"] == 0
