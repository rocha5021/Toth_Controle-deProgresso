from repositories import charm_repo
from services import reference_data, image_cache


def list_charms(character_id):
    active = charm_repo.active_for_character(character_id)
    charms = []
    for charm in reference_data.CHARMS:
        charms.append({
            **charm,
            "ativo": charm["nome"] in active,
            "grade_atual": active.get(charm["nome"]),
            "image_url": image_cache.get_cached_image_url(charm["nome"], "charm"),
        })
    return sorted(charms, key=lambda c: c["prioridade"])


def set_active(character_id, charm_name, active, grade=None):
    charm_repo.set_active(character_id, charm_name, active, grade)
