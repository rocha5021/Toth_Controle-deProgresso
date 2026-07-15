import uuid

from repositories import character_repo
from db import seed as db_seed
from services import image_cache


REQUIRED_FIELDS = ["name", "vocation_hint", "servidor", "level", "focus"]

_OUTFIT_BY_VOCATION = {
    "Elite Knight": "Knight", "Royal Paladin": "Hunter",
    "Master Sorcerer": "Sorcerer", "Elder Druid": "Druid",
}


def list_characters():
    return character_repo.list_all()


def create_character(name, vocation_hint, servidor, level, focus):
    """Cria um personagem novo com as 5 respostas obrigatorias, com
    roadmap em branco pronto (mesmo padrao do Tio Musga)."""
    character_id = "char_" + uuid.uuid4().hex[:10]
    role = {
        "Elite Knight": "EK", "Royal Paladin": "RP", "Master Sorcerer": "MS",
        "Elder Druid": "ED",
    }.get(vocation_hint, vocation_hint[:2].upper())
    outfit_name = _OUTFIT_BY_VOCATION.get(vocation_hint)
    outfit_url = image_cache.get_image_url(outfit_name, "creature") if outfit_name else None
    character_repo.create({
        "id": character_id, "name": name, "role": role,
        "label": f"{name} ({role})", "vocation_hint": vocation_hint,
        "focus": f"{focus} (servidor: {servidor}, level inicial: {level})",
        "accent_color": "#9085e9", "outfit_image_url": outfit_url,
    })
    db_seed.seed_roadmap_for_character(character_id)
    return character_id
