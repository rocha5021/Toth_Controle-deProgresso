from db.connection import get_connection


def farm_log_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM boss_farm_log WHERE character_id = ?",
        (character_id,),
    ).fetchall()
    return {r["boss_name"]: r["last_farmed_date"] for r in rows}


def mark_farmed(character_id, boss_name, date_iso):
    conn = get_connection()
    conn.execute(
        """INSERT INTO boss_farm_log (character_id, boss_name, last_farmed_date)
           VALUES (?, ?, ?)
           ON CONFLICT(character_id, boss_name)
           DO UPDATE SET last_farmed_date = excluded.last_farmed_date""",
        (character_id, boss_name, date_iso),
    )
    conn.commit()
