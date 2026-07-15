"""
Dados de referencia (bosses, charms, bestiary) portados do dashboard web
anterior (legacy_web_dashboard/ek_management_system/data.py). Sao dados
estimados de planejamento - o texto do dashboard antigo ja avisava disso -
valide in-game antes de decisoes importantes.
"""
from pathlib import Path

_BESTIARY_RAW_FILE = (
    Path(__file__).parent.parent.parent
    / "legacy_web_dashboard" / "ek_management_system" / "imports" / "bestiary_raw.txt"
)

_all_creature_names_cache = None


def all_creature_names():
    """Lista mestre com o nome de todas as criaturas do jogo - o export do
    Cyclopedia do Haxta lista TODAS as criaturas (mesmo as com 0 kills),
    entao serve como catalogo completo, independente do personagem."""
    global _all_creature_names_cache
    if _all_creature_names_cache is not None:
        return _all_creature_names_cache
    names = []
    if _BESTIARY_RAW_FILE.exists():
        with open(_BESTIARY_RAW_FILE, encoding="utf-8") as f:
            next(f, None)
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 5:
                    names.append(parts[2].strip())
    _all_creature_names_cache = names
    return names

# Roster completo do Bosstiary (315 bosses, tiers Bane/Archfoe/Nemesis),
# extraido de tibiawiki.com.br/wiki/Bosstiário - fonte real do jogo, nao
# mais uma lista curada de 30. cooldown_dias e uma estimativa generica
# (Bosstiary nao publica cooldown fixo por boss) so para o farm tracker
# ter uma referencia de "quando voltar" - vale validar in-game.
_BOSSTIARY_SOURCE_FILE = Path(__file__).parent.parent / "data" / "bosstiary_source.json"
_DEFAULT_COOLDOWN_DIAS = 20


def build_bosses():
    import json
    if not _BOSSTIARY_SOURCE_FILE.exists():
        return []
    with open(_BOSSTIARY_SOURCE_FILE, encoding="utf-8") as f:
        raw = json.load(f)
    return [
        {
            "nome": b["nome"], "tier": b["tier"], "cooldown_dias": _DEFAULT_COOLDOWN_DIAS,
            "hp": b.get("hp"), "exp": b.get("exp"), "dificuldade": b.get("dificuldade"),
        }
        for b in raw
    ]


BOSSES = build_bosses()


# nome, tipo, custo_cp, efeito, prioridade, quando_desbloquear, onde_usar, status
CHARMS_DB = [
    ("Freeze II", "Ofensivo", 3000, "Chance de dano extra gelo + slow no alvo", 1, "Ja possui", "Hunts com criaturas sem resist gelo (ex: humanoides, undead)", "Ativo"),
    ("Divine Wrath II", "Ofensivo", 3000, "Dano holy em area ao acertar", 1, "Ja possui", "Hunts com demons/undead vulneraveis a holy", "Ativo"),
    ("Savage Blow", "Ofensivo", 1000, "Chance de dano fisico extra em melee", 1, "Ja possui", "Uso geral - qualquer hunt sem resist fisica alta", "Ativo"),
    ("Enflame", "Ofensivo", 1000, "Dano fire em area ao acertar", 2, "Ja possui", "Hunts com criaturas fracas a fire", "Ativo"),
    ("Gut", "Ofensivo", 1000, "Aumenta loot de criaturas (bonus de itens)", 1, "Ja possui", "Farm de loot em geral / Bestiary grind", "Ativo"),
    ("Low Blow", "Ofensivo", 1000, "Dano extra contra alvos com vida alta (bosses)", 2, "Prox. unlock (Bestiary)", "Boss fights - Bosstiary progression", "Planejado"),
    ("Vampiric Fury", "Ofensivo", 3500, "Cura o EK ao acertar - sustain em team hunt", 2, "Apos 3500 CP livres", "Team hunts de alta densidade (Rotten Blood, Asuras)", "Planejado"),
    ("Cripple", "Ofensivo", 1000, "Reduz velocidade do alvo", 3, "Disponivel", "Kiting / controle de adds", "Planejado"),
    ("Parry", "Defensivo", 1000, "Reflete dano fisico recebido", 2, "Disponivel", "Solo hunts com muitos hits fisicos", "Planejado"),
    ("Zap", "Ofensivo", 1000, "Dano energy instantaneo", 3, "Disponivel", "Hunts com fraqueza a energy", "Opcional"),
    ("Curse", "Ofensivo", 1000, "Dano death instantaneo", 3, "Disponivel", "Hunts com fraqueza a death", "Opcional"),
    ("Poison", "Ofensivo", 1000, "Dano earth instantaneo", 3, "Disponivel", "Hunts com fraqueza a earth", "Opcional"),
    ("Wound", "Ofensivo", 1000, "Dano physical instantaneo", 3, "Disponivel", "Uso generico", "Opcional"),
    ("Divine Wrath", "Ofensivo", 1000, "Versao I - upgrade para II", 4, "Ja upada", "-", "Concluido"),
    ("Freeze", "Ofensivo", 1000, "Versao I - upgrade para II", 4, "Ja upada", "-", "Concluido"),
    ("Bless", "Defensivo", 4000, "Revive parcial ao morrer (1x)", 2, "Apos budget de CP", "Hunts de alto risco / bosses dificeis", "Planejado"),
    ("Scavenge", "Utilidade", 3500, "Aumenta gold loot", 3, "Farm de gold puro", "Hunts de lucro (ex: Bosses, Rotten Blood)", "Opcional"),
    ("Cleanse", "Defensivo", 1000, "Remove debuff/paralisia ao ser atingido", 2, "Disponivel", "Hunts com paralisia (Ghouls, Undead)", "Planejado"),
]


def build_charms():
    return [
        {
            "nome": nome, "tipo": tipo, "custo_cp": custo_cp, "efeito": efeito,
            "prioridade": prioridade, "quando_desbloquear": quando, "onde_usar": onde,
            "status": status,
        }
        for nome, tipo, custo_cp, efeito, prioridade, quando, onde, status in CHARMS_DB
    ]


CHARMS = build_charms()


# ---------------------------------------------------------------------------
# EQUIPAMENTOS + METAS - seed inicial do Haxta (EK), roadmap Level 602 -> 1000+
# ---------------------------------------------------------------------------
# prioridade, equipamento, valor_kk (None = ainda nao sabido)
EK_EQUIPAMENTOS_SEED = [
    (1, "Sanguine Bludgeon", 19),
    (2, "Falcon Greaves", 55),
    (3, "Falcon Plate", 32),
    (4, "Falcon Helmet", 18),
    (5, "Soulwalkers", None),
    (6, "Spiritthorn Helmet", None),
    (7, "Spiritthorn Armor", None),
    (8, "Spiritthorn Legs", None),
]

# titulo, status
EK_METAS_SEED = [
    ("Comprar Falcon Greaves", "Pendente"),
    ("Comprar Falcon Plate", "Pendente"),
    ("Comprar Sanguine Bludgeon", "Pendente"),
    ("Transferir para Inabra", "Planejado"),
    ("Chegar no Level 650", "Em andamento"),
    ("Chegar no Club 100", "Em andamento"),
    ("Club 110", "Pendente"),
    ("Club 120", "Pendente"),
]

PRIORIDADES_META = ["Muito Alta", "Alta", "Media", "Baixa"]
STATUS_META = ["Pendente", "Planejado", "Em andamento", "Concluido"]


def build_equipamentos_seed():
    import uuid
    return [
        {"id": uuid.uuid4().hex, "prioridade": p, "nome": nome, "valor_kk": valor}
        for p, nome, valor in EK_EQUIPAMENTOS_SEED
    ]


def build_metas_seed():
    import uuid
    return [
        {
            "id": uuid.uuid4().hex, "titulo": titulo, "descricao": "", "categoria": "",
            "prioridade": "Media", "data": "", "valor_kk": None, "observacoes": "",
            "status": status,
        }
        for titulo, status in EK_METAS_SEED
    ]
