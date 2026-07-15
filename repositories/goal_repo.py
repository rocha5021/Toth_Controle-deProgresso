from datetime import datetime, timezone

from db.connection import get_connection


def _now():
    return datetime.now(timezone.utc).isoformat()


def list_for_character(character_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM goals WHERE character_id = ? ORDER BY created_at",
        (character_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def create(goal):
    conn = get_connection()
    goal = {**goal, "created_at": _now(), "updated_at": _now()}
    conn.execute(
        """INSERT INTO goals
           (id, character_id, titulo, descricao, categoria, status, prioridade,
            valor_kk, deadline, observacoes, created_at, updated_at)
           VALUES (:id, :character_id, :titulo, :descricao, :categoria, :status, :prioridade,
                   :valor_kk, :deadline, :observacoes, :created_at, :updated_at)""",
        goal,
    )
    conn.commit()


def update(goal_id, fields):
    conn = get_connection()
    fields = {**fields, "updated_at": _now()}
    sets = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE goals SET {sets} WHERE id = ?", (*fields.values(), goal_id))
    conn.commit()


def delete(goal_id):
    conn = get_connection()
    conn.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
