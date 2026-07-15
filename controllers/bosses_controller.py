from datetime import datetime, timezone

from repositories import boss_repo
from services import reference_data, image_cache


def _days_since(iso_date):
    if not iso_date:
        return None
    then = datetime.fromisoformat(iso_date).date()
    return (datetime.now(timezone.utc).date() - then).days


def list_bosses(character_id):
    farm_log = boss_repo.farm_log_for_character(character_id)
    bosses = []
    for boss in reference_data.BOSSES:
        name = boss["nome"]
        last_farmed = farm_log.get(name)
        days = _days_since(last_farmed)
        if days is None:
            status = "Nunca farmado"
        elif days >= boss["cooldown_dias"]:
            status = "Disponível"
        else:
            status = f"Aguardar {boss['cooldown_dias'] - days}d"
        bosses.append({
            **boss,
            "last_farmed": last_farmed,
            "status": status,
            "image_url": image_cache.get_cached_image_url(name, "creature"),
        })
    return bosses


def mark_farmed(character_id, boss_name):
    today = datetime.now(timezone.utc).date().isoformat()
    boss_repo.mark_farmed(character_id, boss_name, today)
