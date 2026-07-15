"""
Seed automatico do banco SQLite - roda so quando o banco esta vazio
(nenhum personagem cadastrado). Popula:
- Os 2 personagens (Haxta/EK, Tio Musga/MS)
- Equipamentos + Metas do Haxta (roadmap Level 602 -> 1000+ ja pedido)
- Roadmap em 9 etapas (602 a 1000+) para os dois personagens - do Haxta
  com os campos que ja fazem sentido, do Tio Musga tudo em branco
- Bestiary do Haxta a partir do export REAL do Cyclopedia dele
  (legacy_web_dashboard/ek_management_system/imports/bestiary_raw.txt) -
  nao comeca do zero, usa o progresso que ele ja tem no jogo.
"""
import re
import uuid
from pathlib import Path

from repositories import character_repo, equipment_repo, goal_repo, roadmap_repo, bestiary_repo
from services import reference_data, image_cache

BESTIARY_RAW_FILE = (
    Path(__file__).parent.parent.parent
    / "legacy_web_dashboard" / "ek_management_system" / "imports" / "bestiary_raw.txt"
)

ROADMAP_STEPS = [
    (602, 650), (650, 700), (700, 750), (750, 800),
    (800, 850), (850, 900), (900, 950), (950, 1000), (1000, None),
]


def _parse_bestiary_raw():
    if not BESTIARY_RAW_FILE.exists():
        return []
    entries = []
    with open(BESTIARY_RAW_FILE, encoding="utf-8") as f:
        next(f, None)  # cabecalho
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 5:
                continue
            _step, kills_raw, name, mastery, _echo = parts[:5]
            kills = int(re.sub(r"[^\d]", "", kills_raw) or 0)
            entries.append({
                "nome": name.strip(),
                "kills": kills,
                "mastery_unlocked": "unlocked" in mastery.lower(),
            })
    return entries


def _seed_characters():
    # "Knight"/"Sorcerer" sao os outfits reais mais proximos do pedido
    # (armadura guerreiro / vestes de mago) - nao existe um outfit chamado
    # exatamente "Gold" ou "Mage" na TibiaWiki, ver CHECKLIST.md.
    character_repo.create({
        "id": "ek_haxta", "name": "Haxta", "role": "EK", "label": "Haxta (EK)",
        "vocation_hint": "Elite Knight",
        "focus": "Lucro (menor gasto possivel), itens por level, rotacao de bosses, bestiary, charms, quest",
        "accent_color": "#d4af37",
        "outfit_image_url": image_cache.get_image_url("Knight", "creature"),
    })
    character_repo.create({
        "id": "ms_tiomusga", "name": "Tio Musga", "role": "MS", "label": "Tio Musga (MS)",
        "vocation_hint": "Master Sorcerer",
        "focus": "Bestiary, PvP/GvG quando necessario, treino de ML, hunt em PT (futuro), quest",
        "accent_color": "#7ab4f2",
        "outfit_image_url": image_cache.get_image_url("Sorcerer", "creature"),
    })


def seed_roadmap_for_character(character_id):
    for ordem, (inicio, fim) in enumerate(ROADMAP_STEPS, start=1):
        roadmap_repo.create({
            "id": uuid.uuid4().hex,
            "character_id": character_id,
            "ordem": ordem,
            "nivel_inicio": inicio,
            "nivel_fim": fim,
            "meta_financeira": "",
            "meta_equipamentos": "",
            "meta_skill": "",
            "meta_bosses": "",
            "meta_hunts": "",
            "status": "Pendente" if ordem > 1 else "Em andamento",
            "progresso_pct": 0,
            "concluido": 0,
        })


def _seed_haxta_planning():
    for item in reference_data.build_equipamentos_seed():
        equipment_repo.create({
            "id": item["id"], "character_id": "ek_haxta",
            "prioridade": item["prioridade"], "nome": item["nome"], "valor_kk": item["valor_kk"],
            "categoria": "Equipamento", "status": "Pendente",
            "roi_preco": item["valor_kk"], "roi_beneficio": "", "roi_impacto": "",
            "observacoes": "",
        })
    for meta in reference_data.build_metas_seed():
        goal_repo.create({
            "id": meta["id"], "character_id": "ek_haxta", "titulo": meta["titulo"],
            "descricao": meta["descricao"], "categoria": "Outros",
            "status": meta["status"], "prioridade": meta["prioridade"],
            "valor_kk": meta["valor_kk"], "deadline": meta["data"] or None,
            "observacoes": meta["observacoes"],
        })


def run_seed_if_needed():
    from db.connection import is_fresh_database
    if not is_fresh_database():
        return
    _seed_characters()
    _seed_haxta_planning()
    seed_roadmap_for_character("ek_haxta")
    seed_roadmap_for_character("ms_tiomusga")
    bestiary_entries = _parse_bestiary_raw()
    if bestiary_entries:
        bestiary_repo.bulk_seed("ek_haxta", bestiary_entries)
