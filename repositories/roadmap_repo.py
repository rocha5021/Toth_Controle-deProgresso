from db.connection import get_connection


def list_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM roadmap_steps WHERE character_id = ? ORDER BY ordem",
        (character_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def create(step):
    conn = get_connection()
    conn.execute(
        """INSERT INTO roadmap_steps
           (id, character_id, ordem, nivel_inicio, nivel_fim, meta_financeira,
            meta_equipamentos, meta_skill, meta_bosses, meta_hunts, status,
            progresso_pct, concluido)
           VALUES (:id, :character_id, :ordem, :nivel_inicio, :nivel_fim, :meta_financeira,
                   :meta_equipamentos, :meta_skill, :meta_bosses, :meta_hunts, :status,
                   :progresso_pct, :concluido)""",
        step,
    )
    conn.commit()


def update(step_id, fields):
    conn = get_connection()
    sets = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE roadmap_steps SET {sets} WHERE id = ?", (*fields.values(), step_id))
    conn.commit()
