from db.connection import get_connection


def list_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM bestiary_progress WHERE character_id = ?",
        (character_id,),
    ).fetchall()
    return {r["creature_name"]: dict(r) for r in rows}


def upsert(character_id, creature_name, kills, mastery_unlocked):
    conn = get_connection()
    conn.execute(
        """INSERT INTO bestiary_progress (character_id, creature_name, kills, mastery_unlocked)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(character_id, creature_name)
           DO UPDATE SET kills = excluded.kills, mastery_unlocked = excluded.mastery_unlocked""",
        (character_id, creature_name, kills, int(mastery_unlocked)),
    )
    conn.commit()


def bulk_seed(character_id, entries):
    """entries: lista de dicts {nome, kills, mastery_unlocked}. Usado no seed inicial."""
    conn = get_connection()
    conn.executemany(
        """INSERT OR IGNORE INTO bestiary_progress (character_id, creature_name, kills, mastery_unlocked)
           VALUES (?, ?, ?, ?)""",
        [(character_id, e["nome"], e["kills"], int(e["mastery_unlocked"])) for e in entries],
    )
    conn.commit()
