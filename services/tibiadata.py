"""
Cliente fino para a TibiaData API v4 (https://api.tibiadata.com).
Nao ha API oficial da CipSoft - TibiaData e um projeto comunitario que
espelha os dados publicos de tibia.com em JSON.
"""
import urllib.parse
import urllib.request
import json
from concurrent.futures import ThreadPoolExecutor

BASE = "https://api.tibiadata.com/v4"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EK-Management-System/1.0"

# So essas 5 vocacoes "promovidas" contam pra rankings de nivel alto -
# as variantes sem promocao (Knight/Paladin/Sorcerer/Druid/Monk) sao de
# personagens baixos que ainda nao promoveram e nao fazem sentido num
# Top Level (poluem a lista sem agregar valor).
VALID_VOCATIONS = {
    "Elite Knight", "Royal Paladin", "Master Sorcerer", "Elder Druid", "Exalted Monk",
}


def _get(path):
    url = f"{BASE}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def get_character(name):
    """Retorna a ficha completa e atual de um personagem, direto do tibia.com."""
    enc = urllib.parse.quote(name)
    data = _get(f"character/{enc}")
    char = data.get("character", {}).get("character")
    if not char:
        return None
    deaths = data.get("character", {}).get("deaths", []) or []
    return {
        "name": char.get("name"),
        "level": char.get("level"),
        "vocation": char.get("vocation"),
        "sex": char.get("sex"),
        "world": char.get("world"),
        "residence": char.get("residence"),
        "guild": (char.get("guild") or {}).get("name"),
        "achievement_points": char.get("achievement_points"),
        "account_status": char.get("account_status"),
        "last_login": char.get("last_login"),
        "married_to": char.get("married_to"),
        "houses": char.get("houses", []),
        "deaths": [
            {
                "time": d.get("time"),
                "level": d.get("level"),
                "reason": d.get("reason"),
            }
            for d in deaths[:10]
        ],
    }


def get_worlds():
    data = _get("worlds")
    return [w["name"] for w in data["worlds"]["regular_worlds"]]


def get_latest_news(limit=30):
    """Noticias/atualizacoes oficiais do Tibia (patch notes, eventos etc),
    direto do tibia.com via TibiaData - real, sem scraping."""
    data = _get("news/latest")
    news = data.get("news", [])
    return [
        {
            "id": n.get("id"),
            "date": n.get("date"),
            "title": n.get("news"),
            "category": n.get("category"),
            "type": n.get("type"),
            "url": n.get("url"),
        }
        for n in news[:limit]
    ]


def _fetch_one_world(world):
    try:
        data = _get(f"highscores/{world}/experience/all/1")
        lst = data.get("highscores", {}).get("highscore_list", [])
        return [
            {
                "name": entry["name"],
                "level": entry["level"],
                "vocation": entry.get("vocation", ""),
                "world": world,
                "points": entry.get("value"),
            }
            for entry in lst
        ]
    except Exception:
        return []


def _fetch_highscore_pool(world_list=None, max_workers=16):
    """
    Nao existe highscore global de level (nem filtro por vocacao) na
    TibiaData API v4 - so por mundo, so 'all'. Entao varremos a pagina 1
    (ate 50 entradas) do highscore de 'experience' de cada mundo, em
    PARALELO (senao ~93 requests sequenciais levam mais de 2 minutos e
    a tela fica parecendo travada) - e formamos um pool que da pra usar
    tanto pro Top N global quanto pro Top N por vocacao/mundo, sem
    nenhum request a mais.
    """
    worlds = world_list or get_worlds()
    pool = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for entries in executor.map(_fetch_one_world, worlds):
            pool.extend(entries)
    return pool


def get_top_levels(limit=3, world_list=None, pool=None, only_valid_vocations=True):
    pool = pool if pool is not None else _fetch_highscore_pool(world_list)
    if only_valid_vocations:
        pool = [e for e in pool if e["vocation"] in VALID_VOCATIONS]
    return sorted(pool, key=lambda x: -x["level"])[:limit]


def get_top_levels_by_vocation(limit=20, world_list=None, pool=None, only_valid_vocations=True):
    """Retorna {vocacao: [top N do pool]} - reusa o mesmo pool de
    get_top_levels se for passado, pra nao duplicar as requests."""
    pool = pool if pool is not None else _fetch_highscore_pool(world_list)
    if only_valid_vocations:
        pool = [e for e in pool if e["vocation"] in VALID_VOCATIONS]
    by_vocation = {}
    for entry in pool:
        by_vocation.setdefault(entry["vocation"], []).append(entry)
    return {
        voc: sorted(entries, key=lambda x: -x["level"])[:limit]
        for voc, entries in by_vocation.items()
    }
