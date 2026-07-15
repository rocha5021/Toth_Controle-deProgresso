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


def get_top_levels(limit=3, world_list=None, pause=0.12):
    """
    Nao existe highscore global de level na TibiaData API (so por mundo).
    Entao varremos o highscore de 'experience' (equivalente a level) de
    cada mundo, pegamos o #1 de cada um e ordenamos globalmente.
    """
    worlds = world_list or get_worlds()
    best = []
    for w in worlds:
        try:
            data = _get(f"highscores/{w}/experience/all/1")
            lst = data.get("highscores", {}).get("highscore_list", [])
            if lst:
                top = lst[0]
                best.append({
                    "name": top["name"],
                    "level": top["level"],
                    "vocation": top.get("vocation", ""),
                    "world": w,
                    "points": top.get("value"),
                })
        except Exception:
            pass
        time.sleep(pause)
    best.sort(key=lambda x: -x["level"])
    return best[:limit]
