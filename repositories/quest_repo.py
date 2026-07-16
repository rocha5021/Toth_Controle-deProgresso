from db.connection import get_connection


def completed_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT quest_name, completed_at FROM quests_completed WHERE character_id = ?",
        (character_id,),
    ).fetchall()
    return {r["quest_name"]: r["completed_at"] for r in rows}


def set_completed(character_id, quest_name, completed, completed_at=None):
    conn = get_connection()
    if completed:
        conn.execute(
            """INSERT OR IGNORE INTO quests_completed (character_id, quest_name, completed_at)
               VALUES (?, ?, ?)""",
            (character_id, quest_name, completed_at),
        )
    else:
        conn.execute(
            "DELETE FROM quests_completed WHERE character_id = ? AND quest_name = ?",
            (character_id, quest_name),
        )
    conn.commit()


def bulk_seed(character_id, quest_names):
    conn = get_connection()
    conn.executemany(
        "INSERT OR IGNORE INTO quests_completed (character_id, quest_name, completed_at) VALUES (?, ?, NULL)",
        [(character_id, name) for name in quest_names],
    )
    conn.commit()
