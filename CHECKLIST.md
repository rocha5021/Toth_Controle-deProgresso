# Thoth — Checklist do Projeto

App desktop Python (PySide6/Qt) para gerenciar personagens de Tibia:
- **Haxta (EK)** — Elite Knight, foco em **lucro** (menor gasto possível).
- **Tio Musga (MS)** — Master Sorcerer, foco em **Bestiary / PvP-GvG / ML**.
- Suporta **N personagens** (botão "+ Novo Personagem").

Este arquivo é o histórico vivo de tudo que já foi pedido, decidido e construído.
Atualizar sempre que uma nova solicitação chegar ou um item for concluído.

---

## ✅ Concluído

### Fundação (arquitetura em camadas + SQLite)
- [x] **Banco SQLite** (`data/thoth.db`) substitui os arquivos JSON por personagem.
      Tabelas: `characters`, `equipment_planning`, `goals`, `roadmap_steps`,
      `bestiary_progress`, `boss_farm_log`, `charms_active`.
- [x] **Arquitetura em camadas**: `db/` (conexão+schema+seed) → `repositories/`
      (CRUD puro por tabela) → `services/` (regras de negócio - progresso,
      status derivado) → `controllers/` (orquestram repo+service pras views) →
      `app/views/` (só UI, sem lógica de negócio direto na tela).
- [x] **Seed automático** quando o banco está vazio: personagens, equipamentos e
      metas do Haxta, roadmap de 9 etapas (602→1000+) pros dois, e o **bestiary
      real do Haxta** — usa o export verdadeiro do Cyclopedia dele
      (`bestiary_raw.txt`, 645 criaturas com kills reais), não começa do zero.
- [x] Corrigido um bug real do protótipo anterior (JSON): estado salvo antes de
      um campo novo existir perdia o seed ao recarregar.

### Conteúdo completo (resolvendo o "app vazio/incompleto")
- [x] **Bestiary** — sai de placeholder pra tela real: 645 criaturas, imagem
      real (97.8% resolvida), filtro por status (Completo/Em andamento/
      Pendente), busca por nome, **contador de mortes editável (+/-) por
      criatura, por personagem**. Haxta já mostra os kills reais dele.
- [x] **Bosses** — roster **completo** do Bosstiary (315 bosses reais, tiers
      Bane/Archfoe/Nemesis — extraído da própria TibiaWiki, não mais uma
      lista curada de 30), com imagem real (315/315), busca, filtro por tier,
      e farm/cooldown por personagem.
- [x] **Charms** — 18 charms com imagem real e seleção de "ativos" por personagem.

### Performance de imagens
- [x] Bug de performance real corrigido: baixar ~1000 imagens sequencialmente
      travava a tela por minutos. Agora: cache em **disco** (persiste entre
      execuções) + download em **paralelo** (32 threads) antes de renderizar
      a tabela. Resultado: 1ª vez ~7s (Bestiary, 645 itens), depois ~0.3s.

### Planejamento Estratégico (novo módulo, substitui Equipamentos/Metas soltos)
- [x] Página única com 3 sub-abas (Ficha / Roadmap / Objetivos) — mantém a UI
      simples em vez de empilhar tudo, como pedido.
  - **Ficha**: resumo do personagem + etapa atual do roadmap.
  - **Roadmap**: timeline editável 602→650→...→1000+, cada etapa com meta
    financeira/equipamentos/skill/bosses/hunts + checkbox Concluído +
    progresso calculado automaticamente. Já funciona pro Tio Musga também
    (campos em branco, editável e salvo, como pedido).
  - **Objetivos**: Equipamentos (Adicionar/Editar/Excluir/Duplicar/Mover) +
    Metas (modal "Nova Meta" com Categoria/Prioridade colorida/Data/Valor/
    Observações), ambos com todos os itens originais pré-cadastrados.
- [x] ROI: campos capturados (preço/benefício/impacto) — **cálculo de score
      automático fica pro próximo round** (fazer certo precisa de dados de
      "benefício" que ainda não coletamos consistentemente).

### Personagens
- [x] **Botão "+ Novo Personagem"**: modal com 5 perguntas obrigatórias (nome
      real do Tibia, vocação, servidor, level atual, foco principal). Cria o
      personagem no banco com roadmap vazio pronto pra preencher, e o
      seletor de personagem no topo agora é **dinâmico** (não mais fixo em 2).
- [x] **Retrato dos personagens**: ícone de outfit real ao lado do nome no
      seletor. Não existe outfit chamado exatamente "Gold"/"Mage" na
      TibiaWiki — usei os mais próximos reais disponíveis: **"Knight"**
      (armadura) pro EK e **"Sorcerer"** (vestes de mago) pro MS/novos
      personagens por vocação. Se você souber o nome exato do outfit que
      queria, me diga e eu troco.

### Top Level
- [x] **Top 20 global + Top 20 por vocação** (não mais só Top 3). Descoberta:
      a TibiaData API **não filtra highscores por vocação** (só aceita
      `all`) — contornado buscando a página inteira (até 50 por mundo, que
      já buscávamos mesmo pra pegar só o #1) e montando os rankings a partir
      desse mesmo pool, **sem nenhuma requisição a mais**. Filtro por
      vocação disponível na aba Personagem.

### Infra / distribuição
- [x] Ícone (`app/thoth_icon.ico`) + atalho **Thoth.lnk** na área de trabalho
      (abre sem terminal, via `pythonw.exe`).
- [x] Repositório GitHub: **https://github.com/rocha5021/Toth_Controle-deProgresso**

### Sessão de correções (bugs relatados pelo usuário)
- [x] **"Dados não atualizam" — causa raiz encontrada e corrigida**: a busca
      dos 93 mundos era sequencial e levava **132 segundos**, então parecia
      travado (não era um bug de fato, só lento demais sem indicar isso
      claramente). Paralelizado (16 threads) — agora leva **~10 segundos**.
- [x] **Vocações erradas na lista Top Level** — a TibiaData API retorna
      também as vocações "não promovidas" (Knight/Sorcerer/Druid/Paladin/
      Monk, de personagens baixos), que não fazem sentido num ranking de
      nível alto. Filtrado pra só as **5 vocações reais**: Elite Knight,
      Royal Paladin, Master Sorcerer, Elder Druid, Exalted Monk.
- [x] **Filtro de servidor** adicionado ao lado do filtro de vocação na aba
      Personagem — os dois combinam (ex: Top 20 Elder Druid só da Antica).
- [x] **Mural de Notícias** — aba nova com as atualizações oficiais do Tibia
      (patch notes, eventos) direto do tibia.com via TibiaData API
      (`/v4/news/latest` — real, sem scraping), com botão pra abrir a
      notícia completa no navegador.
- [x] **Quests vazia mesmo após "passar os dados"** — não é bug: eu nunca
      recebi nenhuma lista de quests nesta conversa. Atualizei o texto da
      aba pra deixar isso explícito (antes só dizia "em construção", o que
      confundiu). Quando você mandar a lista (Haxta e Tio Musga), eu
      populo de verdade.
- [x] **Hunts vazia** — não é bug, já era esperado/documentado: a aba
      Hunts depende de um motor de custo/lucro que ainda não existe (ver
      pendências). O texto da aba já explica isso.

## ⏸️ Avaliado e adiado deliberadamente (pedido explícito: só fazer o que gera valor)

- **Relógio digital com animal do Tibia** — decorativo, não ajuda a gerenciar
  progresso. Não construído a menos que você reforce que quer.
- **Conversor TibiaCoins → kk** — não existe fonte oficial de cotação (preço
  de mercado entre jogadores, varia por servidor/dia); exigiria um campo de
  cotação manual. Baixo valor imediato, fica pro próximo round se você quiser.
- **Bloco 3 do Planejamento (Patrimônio/Financeiro + gráfico)** — precisa de
  um modelo de dados novo (gold atual, lucro diário/semanal/mensal) que não
  existe ainda em lugar nenhum do app — é um subsistema novo, não um ajuste.
- **Exportar Excel/PDF/JSON e Importar JSON** — fica bem mais simples agora
  que os dados estão no SQLite (é essencialmente um `SELECT` + serializar).
  Fica como polish depois que o Planejamento estiver mais maduro.
- **Dashboard de KPIs e progress bars globais** — depende dos dados do
  Planejamento estarem mais completos primeiro (senão mostra 0% em tudo).

## 🚧 Pendente (não descartado, só ainda não priorizado)

- [ ] **Aba "Treino de Skill"** (pedido, inspirado no
      [intibia.com/exercise-weapons-calculator](https://intibia.com/pt/tools/exercise-weapons-calculator)):
      calculadora de quantas exercise weapons/horas faltam pra sair do
      skill atual até um alvo. **Pesquisei bastante e não achei a fórmula
      exata de crescimento de skill numa fonte confiável** (as calculadoras
      são JS client-side, a fórmula não fica exposta no HTML/wiki). O que
      confirmei com segurança: os tipos de exercise weapon e suas
      cargas/durações reais — Training (50 usos, 1min40s), Regular (500
      usos, 16min40s), Durable (1.800 usos, 1h), Lasting (14.400 usos, 8h).
      **Não implementei o cálculo pra não arriscar te dar um número
      errado numa ferramenta que devia ser confiável** — preciso validar
      a fórmula certa com você antes (ou você já ter uma fonte confirmada).
- [ ] **Hunts do EK** — motor de sugestão priorizando lucro líquido com o
      menor gasto possível. Precisa desenhar uma estimativa de custo
      (supplies) por hunt — hoje não existe esse campo em lugar nenhum.
- [ ] **Quests** — tracker vazio, pronto pra receber a lista que o usuário
      vai enviar com as quests já concluídas de Haxta e Tio Musga.
- [ ] **MS (Tio Musga)**: seção específica de PvP/GvG e treino de Magic Level.
- [ ] **Armas (Club) + Equipamentos gerais** (referência, não confundir com a
      lista de compras do Planejamento) — existiam no dashboard antigo,
      ainda não portados.
- [ ] **Renomear pasta `Planilha` → `Hermes`** — bloqueado: VS Code com a
      pasta aberta trava o rename no Windows.
- [ ] Dashboard antigo tinha também: visão geral, Upgrade Advisor, Wheel of
      Destiny, Checklist Diário, Transferência Peloria→Inabra — específicos
      do contexto de 1 personagem só; avaliar se ainda fazem sentido no
      formato multi-personagem antes de portar.

## 🗑️ Descartado / revertido

- Character Bazaar (Trade) — implementado no dashboard web e depois removido
  a pedido do usuário.
- Dashboard web em HTML/JS — não descartado, **substituído** como frente
  principal de desenvolvimento; arquivado em `legacy_web_dashboard/`.
- Persistência em JSON por personagem (`services/storage.py` antigo) —
  substituída pelo SQLite (`db/` + `repositories/`). `services/storage.py`
  agora só guarda o cache de dados externos (TibiaData API), que não é
  "dado do usuário".

## 🔗 Links e referências técnicas úteis

- TibiaData API: `https://api.tibiadata.com/v4/character/<nome>`,
  `.../v4/worlds`, `.../v4/highscores/<mundo>/experience/all/1` — sem API
  key, mas instável às vezes (502/503 intermitente, visto na prática).
  **Não filtra por vocação** (só `all`) — contornado, ver Top Level acima.
- TibiaWiki Brasil (imagens de itens/criaturas): link direto via
  `.../wiki/Especial:FilePath/<Arquivo>.gif`, sem Cloudflare.
- TibiaWiki Bosstiário (roster completo de bosses): página única com 3
  tabelas (Bane/Archfoe/Nemesis), imagem já embutida no HTML de cada linha.
- Notícias oficiais: `https://api.tibiadata.com/v4/news/latest` — mesmo dado
  de `tibia.com/news`, mas em JSON real, sem precisar contornar Cloudflare.
- Repositório do Thoth: `https://github.com/rocha5021/Toth_Controle-deProgresso`

### Sites analisados a pedido do usuário (o que rendeu valor)
- **tibia.com/news** — não dava pra usar direto (Cloudflare), mas achei o
  mesmo conteúdo real via TibiaData API (`/v4/news/latest`) → virou o
  Mural de Notícias.
- **tibiawiki.com.br/wiki/Home** — já é a fonte usada pra praticamente
  todas as imagens do app (Bestiary/Bosses/Charms) e pro roster completo
  de bosses; não achei conteúdo novo de valor além do que já exploramos.
- **intibia.com/exercise-weapons-calculator** — inspirou o pedido de aba
  de Treino de Skill; dados confiáveis de exercise weapons confirmados
  (ver pendências), fórmula de crescimento de skill ainda não confirmada.

## Pastas do projeto

- `Planilha/legacy_web_dashboard/` — dashboard web antigo, arquivado, intacto.
- `Planilha/Thoth/` — app novo, em desenvolvimento ativo (também no GitHub).
- `Planilha/EK_Management_System.xlsx` — planilha original, na raiz.
- Pendente renomear `Planilha/` → `Hermes/` (bloqueado pelo VS Code).

## Nota sobre verificação visual

A automação de clique via UI Automation (Windows) se mostrou instável nesta
máquina — já derrubou o app algumas vezes durante testes (sem relação com
bugs reais do app: os mesmos fluxos passam limpos em testes headless). Por
isso a prática desta sessão foi: validar tudo primeiro sem interface
(`QT_QPA_PLATFORM=offscreen`), e usar screenshot real só como confirmação
leve final, sem insistir em automação de clique quando ela mesma trava.
