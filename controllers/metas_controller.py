import uuid

from repositories import goal_repo


def list_goals(character_id):
    return goal_repo.list_for_character(character_id)


def add_goal(character_id, data):
    goal_repo.create({"id": uuid.uuid4().hex, "character_id": character_id, "status": "Pendente", **data})


def update_goal(goal_id, fields):
    goal_repo.update(goal_id, fields)


def delete_goal(goal_id):
    goal_repo.delete(goal_id)


def set_status(goal_id, status):
    goal_repo.update(goal_id, {"status": status})
