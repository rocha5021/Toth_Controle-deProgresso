"""
Cliente fino para a TibiaData API v4 (https://api.tibiadata.com).
Nao ha API oficial da CipSoft - TibiaData e um projeto comunitario que
espelha os dados publicos de tibia.com em JSON.
"""
import time
import urllib.parse
import urllib.request
import json

BASE = "https://api.tibiadata.com/v4"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EK-Management-System/1.0"


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


def _fetch_highscore_pool(world_list=None, pause=0.12):
    """
    Nao existe highscore global de level (nem filtro por vocacao) na
    TibiaData API v4 - so por mundo, so 'all'. Entao varremos a pagina 1
    (ate 50 entradas) do highscore de 'experience' de cada mundo - o
    mesmo dado que ja buscavamos, so que aproveitando a lista inteira em
    vez de so o #1 - e formamos um pool que da pra usar tanto pro Top N
    global quanto pro Top N por vocacao, sem nenhum request a mais.
    """
    worlds = world_list or get_worlds()
    pool = []
    for w in worlds:
        try:
            data = _get(f"highscores/{w}/experience/all/1")
            lst = data.get("highscores", {}).get("highscore_list", [])
            for entry in lst:
                pool.append({
                    "name": entry["name"],
                    "level": entry["level"],
                    "vocation": entry.get("vocation", ""),
                    "world": w,
                    "points": entry.get("value"),
                })
        except Exception:
            pass
        time.sleep(pause)
    return pool


def get_top_levels(limit=3, world_list=None, pause=0.12, pool=None):
    pool = pool if pool is not None else _fetch_highscore_pool(world_list, pause)
    return sorted(pool, key=lambda x: -x["level"])[:limit]


def get_top_levels_by_vocation(limit=20, world_list=None, pause=0.12, pool=None):
    """Retorna {vocacao: [top N do pool]} - reusa o mesmo pool de
    get_top_levels se for passado, pra nao duplicar as 93 requests."""
    pool = pool if pool is not None else _fetch_highscore_pool(world_list, pause)
    by_vocation = {}
    for entry in pool:
        by_vocation.setdefault(entry["vocation"], []).append(entry)
    return {
        voc: sorted(entries, key=lambda x: -x["level"])[:limit]
        for voc, entries in by_vocation.items()
    }
