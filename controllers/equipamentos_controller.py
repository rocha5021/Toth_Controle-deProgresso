import uuid

from repositories import equipment_repo


def list_items(character_id):
    return equipment_repo.list_for_character(character_id)


def add_item(character_id, nome="Novo item", valor_kk=None, categoria="Equipamento"):
    items = equipment_repo.list_for_character(character_id)
    equipment_repo.create({
        "id": uuid.uuid4().hex, "character_id": character_id,
        "prioridade": len(items) + 1, "nome": nome, "valor_kk": valor_kk,
        "categoria": categoria, "status": "Pendente",
        "roi_preco": valor_kk, "roi_beneficio": "", "roi_impacto": "",
        "observacoes": "",
    })


def update_field(item_id, field, value):
    equipment_repo.update(item_id, {field: value})


def duplicate(character_id, item_id):
    items = equipment_repo.list_for_character(character_id)
    original = next(i for i in items if i["id"] == item_id)
    equipment_repo.create({
        **original,
        "id": uuid.uuid4().hex,
        "nome": original["nome"] + " (cópia)",
        "prioridade": len(items) + 1,
    })


def delete(item_id):
    equipment_repo.delete(item_id)


def move(character_id, item_id, direction):
    items = equipment_repo.list_for_character(character_id)
    ids = [i["id"] for i in items]
    idx = ids.index(item_id)
    new_idx = idx + direction
    if 0 <= new_idx < len(ids):
        ids[idx], ids[new_idx] = ids[new_idx], ids[idx]
        equipment_repo.reorder(character_id, ids)
