"""
Regras de negocio do Planejamento Estrategico - fica fora das views
(Model/Repository so guardam dado, aqui calculamos coisas derivadas).
"""


def bestiary_status(kills, mastery_unlocked):
    if mastery_unlocked:
        return "Completo"
    if kills > 0:
        return "Em andamento"
    return "Pendente"


def roadmap_progress_pct(step):
    """% de progresso de uma etapa do roadmap, com base nos campos de meta
    preenchidos e no checkbox de concluido. Simples e transparente: cada
    meta preenchida conta um quinto, concluido marca 100%."""
    if step.get("concluido"):
        return 100
    campos = [
        step.get("meta_financeira"), step.get("meta_equipamentos"),
        step.get("meta_skill"), step.get("meta_bosses"), step.get("meta_hunts"),
    ]
    preenchidos = sum(1 for c in campos if c and str(c).strip())
    if not preenchidos:
        return 0
    return round(preenchidos / len(campos) * 90)  # nunca bate 100% sem marcar concluido


def equipment_roi_score(preco_kk, impacto):
    """ROI simples: impacto (Baixo/Medio/Alto/Muito Alto) dividido pelo preco.
    So calcula se preco > 0 e impacto reconhecido - senao retorna None (nao
    inventa numero sem base)."""
    impacto_score = {"Baixo": 1, "Medio": 2, "Alto": 3, "Muito Alto": 4}.get(impacto)
    if not preco_kk or preco_kk <= 0 or impacto_score is None:
        return None
    return round(impacto_score / preco_kk, 3)


def planning_summary(equipamentos, metas, roadmap_steps):
    """KPIs simples pro topo da pagina de Planejamento."""
    total_equip = len(equipamentos)
    comprados = sum(1 for e in equipamentos if (e.get("status") or "").lower() == "comprado")
    total_metas = len(metas)
    metas_concluidas = sum(1 for m in metas if (m.get("status") or "").lower() == "concluido")
    total_roadmap = len(roadmap_steps)
    roadmap_concluido = sum(1 for r in roadmap_steps if r.get("concluido"))
    return {
        "equipamentos_pct": round(comprados / total_equip * 100) if total_equip else 0,
        "metas_pct": round(metas_concluidas / total_metas * 100) if total_metas else 0,
        "roadmap_pct": round(roadmap_concluido / total_roadmap * 100) if total_roadmap else 0,
    }
