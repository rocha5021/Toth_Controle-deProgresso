from repositories import bestiary_repo
from services import reference_data, planning_service, image_cache


def list_creatures(character_id):
    """Junta o catalogo mestre de criaturas com o progresso do personagem
    (0/bloqueada por padrao se ele ainda nao registrou nada)."""
    progress = bestiary_repo.list_for_character(character_id)
    creatures = []
    for name in reference_data.all_creature_names():
        p = progress.get(name)
        kills = p["kills"] if p else 0
        mastery = bool(p["mastery_unlocked"]) if p else False
        creatures.append({
            "nome": name,
            "kills": kills,
            "mastery_unlocked": mastery,
            "status": planning_service.bestiary_status(kills, mastery),
            "image_url": image_cache.get_cached_image_url(name, "creature"),
        })
    return creatures


def set_kills(character_id, creature_name, kills, mastery_unlocked=None):
    if mastery_unlocked is None:
        progress = bestiary_repo.list_for_character(character_id).get(creature_name)
        mastery_unlocked = bool(progress["mastery_unlocked"]) if progress else False
    bestiary_repo.upsert(character_id, creature_name, max(0, kills), mastery_unlocked)
