from db.connection import get_connection


def active_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT charm_name, grade FROM charms_active WHERE character_id = ?",
        (character_id,),
    ).fetchall()
    return {r["charm_name"]: r["grade"] for r in rows}


def set_active(character_id, charm_name, active, grade=None):
    conn = get_connection()
    if active:
        conn.execute(
            """INSERT INTO charms_active (character_id, charm_name, grade) VALUES (?, ?, ?)
               ON CONFLICT(character_id, charm_name) DO UPDATE SET grade = excluded.grade""",
            (character_id, charm_name, grade),
        )
    else:
        conn.execute(
            "DELETE FROM charms_active WHERE character_id = ? AND charm_name = ?",
            (character_id, charm_name),
        )
    conn.commit()


def bulk_set_active(character_id, entries):
    """entries: lista de (charm_name, grade). Substitui os charms ativos
    do personagem pelos passados (usado no seed com dados reais)."""
    conn = get_connection()
    conn.execute("DELETE FROM charms_active WHERE character_id = ?", (character_id,))
    conn.executemany(
        "INSERT INTO charms_active (character_id, charm_name, grade) VALUES (?, ?, ?)",
        [(character_id, name, grade) for name, grade in entries],
    )
    conn.commit()
