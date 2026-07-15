from repositories import roadmap_repo
from services import planning_service


def list_steps(character_id):
    steps = roadmap_repo.list_for_character(character_id)
    for step in steps:
        step["progresso_pct"] = planning_service.roadmap_progress_pct(step)
    return steps


def update_step(step_id, fields):
    roadmap_repo.update(step_id, fields)


def toggle_concluido(step_id, concluido):
    roadmap_repo.update(step_id, {"concluido": int(concluido), "status": "Concluido" if concluido else "Em andamento"})
