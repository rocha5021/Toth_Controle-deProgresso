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


def bosstiary_progress_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT boss_name, step, kills FROM bosstiary_progress WHERE character_id = ?",
        (character_id,),
    ).fetchall()
    return {r["boss_name"]: {"step": r["step"], "kills": r["kills"]} for r in rows}


def bulk_seed_bosstiary(character_id, entries):
    """entries: lista de dicts {nome, step, kills}."""
    conn = get_connection()
    conn.executemany(
        """INSERT OR IGNORE INTO bosstiary_progress (character_id, boss_name, step, kills)
           VALUES (?, ?, ?, ?)""",
        [(character_id, e["nome"], e["step"], e["kills"]) for e in entries],
    )
    conn.commit()


def set_bosstiary_progress(character_id, boss_name, step, kills):
    conn = get_connection()
    conn.execute(
        """INSERT INTO bosstiary_progress (character_id, boss_name, step, kills)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(character_id, boss_name)
           DO UPDATE SET step = excluded.step, kills = excluded.kills""",
        (character_id, boss_name, step, kills),
    )
    conn.commit()
