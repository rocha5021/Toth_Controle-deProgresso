from db.connection import get_connection


def list_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM characters ORDER BY rowid").fetchall()
    return [dict(r) for r in rows]


def get(character_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM characters WHERE id = ?", (character_id,)).fetchone()
    return dict(row) if row else None


def create(character):
    conn = get_connection()
    conn.execute(
        """INSERT INTO characters (id, name, role, label, vocation_hint, focus, accent_color, outfit_image_url)
           VALUES (:id, :name, :role, :label, :vocation_hint, :focus, :accent_color, :outfit_image_url)""",
        character,
    )
    conn.commit()


def update(character_id, fields):
    conn = get_connection()
    sets = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE characters SET {sets} WHERE id = ?", (*fields.values(), character_id))
    conn.commit()
