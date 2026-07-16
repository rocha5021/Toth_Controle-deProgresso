from datetime import datetime, timezone

from repositories import boss_repo
from services import reference_data, image_cache

STEP_LABELS = {0: "Nenhum", 1: "Bane", 2: "Archfoe", 3: "Nemesis"}


def _days_since(iso_date):
    if not iso_date:
        return None
    then = datetime.fromisoformat(iso_date).date()
    return (datetime.now(timezone.utc).date() - then).days


def list_bosses(character_id):
    farm_log = boss_repo.farm_log_for_character(character_id)
    # nomes do export do Cyclopedia podem diferir levemente dos nomes da
    # wiki (ex: sufixos) - casa por nome em minusculo pra nao perder dado
    bosstiary_raw = boss_repo.bosstiary_progress_for_character(character_id)
    bosstiary = {name.lower(): progress for name, progress in bosstiary_raw.items()}

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

        progress = bosstiary.get(name.lower(), {"step": 0, "kills": 0})
        bosses.append({
            **boss,
            "last_farmed": last_farmed,
            "status": status,
            "bosstiary_step": progress["step"],
            "bosstiary_step_label": STEP_LABELS.get(progress["step"], "Nenhum"),
            "bosstiary_kills": progress["kills"],
            "image_url": image_cache.get_cached_image_url(name, "creature"),
        })
    return bosses


def mark_farmed(character_id, boss_name):
    today = datetime.now(timezone.utc).date().isoformat()
    boss_repo.mark_farmed(character_id, boss_name, today)


def set_bosstiary_progress(character_id, boss_name, step, kills):
    boss_repo.set_bosstiary_progress(character_id, boss_name, step, kills)
