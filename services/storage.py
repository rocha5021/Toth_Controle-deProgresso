"""
Persistencia local do Thoth: um arquivo JSON por personagem, mais o
cache dos dados reais buscados na TibiaData API.

Cada personagem (ek_haxta, ms_tiomusga) tem seu proprio arquivo em
data/<id>.json - assim bestiary/bosses/charms/quests podem evoluir de
forma independente por personagem (o dashboard web anterior guardava
isso tudo num unico estado compartilhado, o que nao fazia sentido para
dois personagens com objetivos diferentes).
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CHARACTERS_FILE = DATA_DIR / "characters.json"
TRACKED_CACHE_FILE = DATA_DIR / "cache_tracked.json"


def load_characters():
    with open(CHARACTERS_FILE, encoding="utf-8") as f:
        return json.load(f)["characters"]


def _character_file(character_id):
    return DATA_DIR / f"{character_id}.json"


def _default_state(character_id):
    state = {
        "quests_concluidas": [],
        "bestiary_progress": {},
        "boss_farm_log": {},
        "charms_ativos": [],
        "equipamentos": [],
        "metas": [],
    }
    if character_id == "ek_haxta":
        # roadmap Level 602 -> 1000+ do Haxta ja vem pre-preenchido
        from services import reference_data
        state["equipamentos"] = reference_data.build_equipamentos_seed()
        state["metas"] = reference_data.build_metas_seed()
    return state


def load_character_state(character_id):
    """Estado editavel do personagem (quests concluidas, bestiary marcado,
    boss farm log, charms ativos, equipamentos, metas etc). Personagens novos
    comecam vazios, exceto o Haxta que ja vem com o roadmap 602->1000+ seed."""
    path = _character_file(character_id)
    if path.exists():
        with open(path, encoding="utf-8") as f:
            state = json.load(f)
        # garante que estados salvos antes de um campo novo existir nao quebrem
        # (usa o default/seed correto por personagem, nao uma lista vazia generica)
        for key, default in _default_state(character_id).items():
            if key not in state:
                state[key] = default
        return state
    return _default_state(character_id)


def save_character_state(character_id, state):
    with open(_character_file(character_id), "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_tracked_cache():
    if TRACKED_CACHE_FILE.exists():
        with open(TRACKED_CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None


def save_tracked_cache(data):
    with open(TRACKED_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
