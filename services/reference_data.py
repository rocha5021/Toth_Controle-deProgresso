"""
Dados de referencia (bosses, charms) portados do dashboard web anterior
(legacy_web_dashboard/ek_management_system/data.py). Sao dados estimados
de planejamento - o texto do dashboard antigo ja avisava disso - valide
in-game antes de decisoes importantes.
"""

# nome, local, cooldown_dias, chance_loot_raro, lucro_medio_kk, valor_esperado_kk
_BOSS_RAW = [
    ("Malvatrix", "Fenrock", 20, "1/500", 8.5, 0.017),
    ("Bakragore", "Fibula", 20, "1/300", 15.0, 0.05),
    ("Fury Bringer", "Fenrock", 20, "1/400", 6.0, 0.015),
    ("Zamirah", "Fenrock", 20, "1/450", 7.2, 0.016),
    ("Dreaded Ancient Menace", "Fenrock", 20, "1/600", 10.0, 0.017),
    ("Yielothax", "Fenrock", 20, "1/350", 5.5, 0.016),
    ("Silencer", "Fenrock", 20, "1/500", 9.0, 0.018),
    ("Vemiath", "Fenrock", 20, "1/400", 6.8, 0.017),
    ("Nadir", "Fenrock", 20, "1/550", 8.0, 0.015),
    ("Vok the Freakish Guard", "Roshamuul", 20, "1/250", 4.5, 0.018),
    ("Goroma", "Roshamuul", 20, "1/300", 5.0, 0.017),
    ("Kesar the Whipmaster", "Roshamuul", 20, "1/250", 4.0, 0.016),
    ("Diseased Bill", "Roshamuul", 20, "1/150", 2.5, 0.017),
    ("Bones the Chicken", "Roshamuul", 20, "1/100", 1.2, 0.012),
    ("Zeliko Steelsoul", "Vengoth", 20, "1/300", 5.5, 0.018),
    ("Serpseayez", "Cobra Bastion", 20, "1/350", 6.0, 0.017),
    ("Zulazza the Corruptor", "Zao", 20, "1/300", 5.8, 0.019),
    ("Ravager", "Marapur", 20, "1/500", 12.0, 0.024),
    ("Wrathful Nargash", "Marapur", 20, "1/450", 9.5, 0.021),
    ("Lord Retro", "Rookgaard", 20, "1/50", 0.5, 0.01),
    ("Ferumbras", "Ferumbras Citadel", 20, "1/700", 25.0, 0.036),
    ("Ghazbaran", "Ghazbaran's Kingdom", 20, "1/700", 22.0, 0.031),
    ("Orshabaal", "Various", 20, "1/600", 18.0, 0.03),
    ("Morgaroth", "Various", 20, "1/600", 17.0, 0.028),
    ("The Pale Worm", "Falcon Bastion", 20, "1/500", 14.0, 0.028),
    ("Shard of Corruption", "Falcon Bastion", 20, "1/500", 13.5, 0.027),
    ("Grand Mother Foulscale", "Cobra Bastion", 20, "1/400", 9.0, 0.0225),
    ("General Murius", "Cobra Bastion", 20, "1/400", 8.5, 0.021),
    ("Yeti", "Behemoth Isle", 20, "1/200", 3.0, 0.015),
    ("The Welter", "Feyrist", 20, "1/450", 10.0, 0.022),
]


def build_bosses():
    return [
        {
            "nome": nome, "local": local, "cooldown_dias": cd,
            "chance_loot_raro": chance, "lucro_medio_kk": lucro,
            "valor_esperado_kk": round(ev, 3),
        }
        for nome, local, cd, chance, lucro, ev in _BOSS_RAW
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
