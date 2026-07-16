"""
Repository generico pra listas simples de "desbloqueado" por personagem
(Titles, Achievements, Imbuements) - todas tem a mesma forma
(character_id, nome), entao reusa um unico padrao em vez de 3 arquivos
quase identicos.
"""
from db.connection import get_connection

_TABLES = {
    "titles": ("titles_unlocked", "title_name"),
    "achievements": ("achievements_unlocked", "achievement_name"),
    "imbuements": ("imbuements_unlocked", "imbuement_name"),
}


def unlocked_for_character(kind, character_id):
    table, column = _TABLES[kind]
    conn = get_connection()
    rows = conn.execute(
        f"SELECT {column} FROM {table} WHERE character_id = ?",
        (character_id,),
    ).fetchall()
    return {r[column] for r in rows}


def bulk_seed(kind, character_id, names):
    table, column = _TABLES[kind]
    conn = get_connection()
    conn.executemany(
        f"INSERT OR IGNORE INTO {table} (character_id, {column}) VALUES (?, ?)",
        [(character_id, name) for name in names],
    )
    conn.commit()


def set_unlocked(kind, character_id, name, unlocked):
    table, column = _TABLES[kind]
    conn = get_connection()
    if unlocked:
        conn.execute(
            f"INSERT OR IGNORE INTO {table} (character_id, {column}) VALUES (?, ?)",
            (character_id, name),
        )
    else:
        conn.execute(
            f"DELETE FROM {table} WHERE character_id = ? AND {column} = ?",
            (character_id, name),
        )
    conn.commit()
