from datetime import datetime, timezone

from db.connection import get_connection


def _now():
    return datetime.now(timezone.utc).isoformat()


def list_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM equipment_planning WHERE character_id = ? ORDER BY prioridade",
        (character_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def create(item):
    conn = get_connection()
    item = {**item, "created_at": _now(), "updated_at": _now()}
    conn.execute(
        """INSERT INTO equipment_planning
           (id, character_id, prioridade, nome, valor_kk, categoria, status,
            roi_preco, roi_beneficio, roi_impacto, observacoes, created_at, updated_at)
           VALUES (:id, :character_id, :prioridade, :nome, :valor_kk, :categoria, :status,
                   :roi_preco, :roi_beneficio, :roi_impacto, :observacoes, :created_at, :updated_at)""",
        item,
    )
    conn.commit()


def update(item_id, fields):
    conn = get_connection()
    fields = {**fields, "updated_at": _now()}
    sets = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE equipment_planning SET {sets} WHERE id = ?", (*fields.values(), item_id))
    conn.commit()


def delete(item_id):
    conn = get_connection()
    conn.execute("DELETE FROM equipment_planning WHERE id = ?", (item_id,))
    conn.commit()


def reorder(character_id, ordered_ids):
    """Recalcula prioridade (1..N) na ordem dada."""
    conn = get_connection()
    for idx, item_id in enumerate(ordered_ids, start=1):
        conn.execute(
            "UPDATE equipment_planning SET prioridade = ?, updated_at = ? WHERE id = ? AND character_id = ?",
            (idx, _now(), item_id, character_id),
        )
    conn.commit()
