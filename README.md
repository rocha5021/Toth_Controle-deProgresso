# Thoth

App desktop (Python + PySide6/Qt) para gerenciar o progresso de dois personagens de Tibia:

- **Haxta (EK)** — Elite Knight, foco em lucro (menor gasto possível), itens por level,
  rotação de bosses, bestiary, charms, quests.
- **Tio Musga (MS)** — Master Sorcerer, foco em bestiary, PvP/GvG, treino de Magic Level, quests.

Busca dados reais direto da [TibiaData API](https://api.tibiadata.com) (projeto comunitário
que espelha os dados públicos do tibia.com), com atualização automática a cada 3 horas.

## Rodar localmente

```
pip install -r requirements.txt
python main.py
```

## Estrutura

- `app/` — interface (janela principal, views, tema visual)
- `services/` — busca de dados reais (TibiaData API) e persistência local
- `data/` — estado local por personagem (JSON)
- `CHECKLIST.md` — histórico vivo de tudo que já foi pedido/decidido/construído

## Status

Ver [CHECKLIST.md](CHECKLIST.md) para o que já está pronto e o que está pendente.
