from db.connection import get_connection


def active_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT charm_name FROM charms_active WHERE character_id = ?",
        (character_id,),
    ).fetchall()
    return {r["charm_name"] for r in rows}


def set_active(character_id, charm_name, active):
    conn = get_connection()
    if active:
        conn.execute(
            "INSERT OR IGNORE INTO charms_active (character_id, charm_name) VALUES (?, ?)",
            (character_id, charm_name),
        )
    else:
        conn.execute(
            "DELETE FROM charms_active WHERE character_id = ? AND charm_name = ?",
            (character_id, charm_name),
        )
    conn.commit()
