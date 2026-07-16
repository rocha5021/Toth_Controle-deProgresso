from datetime import datetime, timezone

from repositories import quest_repo


def list_quests(character_id):
    completed = quest_repo.completed_for_character(character_id)
    return [
        {"nome": name, "completed_at": completed_at}
        for name, completed_at in sorted(completed.items())
    ]


def add_quest(character_id, quest_name):
    today = datetime.now(timezone.utc).date().isoformat()
    quest_repo.set_completed(character_id, quest_name, True, today)


def remove_quest(character_id, quest_name):
    quest_repo.set_completed(character_id, quest_name, False)
