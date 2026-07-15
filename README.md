# Thoth

App desktop (Python + PySide6/Qt) para gerenciar o progresso de personagens de Tibia:

- **Haxta (EK)** — Elite Knight, foco em lucro (menor gasto possível), itens por level,
  rotação de bosses, bestiary, charms, quests.
- **Tio Musga (MS)** — Master Sorcerer, foco em bestiary, PvP/GvG, treino de Magic Level, quests.
- Suporta personagens adicionais via o botão "+ Novo Personagem".

Busca dados reais direto da [TibiaData API](https://api.tibiadata.com) (projeto comunitário
que espelha os dados públicos do tibia.com), com atualização automática a cada 3 horas, e
imagens reais (itens/criaturas/bosses/charms) linkadas direto da TibiaWiki Brasil.

## Rodar localmente

```
pip install -r requirements.txt
python main.py
```

## Estrutura (arquitetura em camadas)

- `app/` — interface (janela principal, views, tema visual) — só UI, sem regra de negócio
- `controllers/` — orquestram repository + service pras views
- `services/` — regras de negócio (progresso, status) e busca de dados externos (TibiaData API)
- `repositories/` — acesso a dado puro (CRUD) por tabela do SQLite
- `db/` — conexão, schema e seed inicial do banco (`data/thoth.db`)
- `data/` — banco SQLite + caches locais (imagens, dados da API)
- `CHECKLIST.md` — histórico vivo de tudo que já foi pedido/decidido/construído

## Status

Ver [CHECKLIST.md](CHECKLIST.md) para o que já está pronto e o que está pendente.
