# Thoth — Checklist do Projeto

App desktop Python (PySide6/Qt) para gerenciar dois personagens de Tibia:
- **Haxta (EK)** — Elite Knight, foco em **lucro** (menor gasto possível).
- **Tio Musga (MS)** — Master Sorcerer, foco em **Bestiary / PvP-GvG / ML**.

Este arquivo é o histórico vivo de tudo que já foi pedido, decidido e construído.
Atualizar sempre que uma nova solicitação chegar ou um item for concluído.

---

## ✅ Concluído

- [x] Dashboard web (HTML/CSS/JS) original construído em `legacy_web_dashboard/`
      (arquivado, não apagado — o gerador Python `data.py`/`build.py` e o antigo
      servidor Flask também estão lá dentro).
- [x] Conexão com dados reais do Tibia via **TibiaData API** (`api.tibiadata.com`,
      projeto comunitário — não existe API oficial da CipSoft).
- [x] Validado: Haxta = Elite Knight level ~605, mundo Peloria. Tio Musga = Sorcerer
      level 402, mundo Inabra. (Níveis mudam ao vivo — já vimos Haxta subir de
      604→605 durante os testes.)
- [x] Top 3 de level do Tibia calculado varrendo os 93 mundos oficiais via
      highscores de experience (não existe highscore global de level na API):
      **Dejairzin** (3119, Ferobra), **Bobeek** (3082, Bona), **Veyllor** (3055, Gentebra).
      Validado batendo com o highscores oficial do site.
- [x] Character Bazaar (Trade): implementado no dashboard web (scraping via
      Chromium headless, contorna Cloudflare) e depois **removido a pedido do
      usuário** — não é mais prioridade.
- [x] Pesquisa de imagens reais da TibiaWiki Brasil (tibiawiki.com.br):
      - Página normal (`/wiki/<Nome>`) passa pelo desafio Cloudflare via Chromium headless.
      - **Descoberta chave**: `Especial:FilePath/<Arquivo>` redireciona pro
        arquivo estático real (`/images/.../Nome.gif`) e esse caminho **não** fica
        atrás do Cloudflare — dá pra linkar direto sem headless browser e sem
        precisar baixar a imagem.
      - Taxa de acerto testada: Bestiary 59/60, Charms 17/18 (padrão `Nome_Icon.gif`),
        Armas 7/8. Equipamentos e Bosses tiveram taxa menor (nomes não batem
        exatamente com a wiki) — precisa checar nome real por item quando formos
        implementar essa parte.
      - **Pausado** até o core do Thoth estar pronto (ver pendências).
- [x] Decisão: recomeçar como **app desktop 100% Python** (não navegador/JS).
      Motivo do usuário: consistência de stack + quer gravar vídeos/cortes pra
      redes sociais mostrando o app, quer algo mais "profissional".
- [x] Nome escolhido: **Thoth** (deus egípcio da sabedoria e do registro de
      conhecimento). Framework: **PySide6 (Qt)**.
- [x] Estrutura do projeto criada (`Thoth/app`, `Thoth/services`, `Thoth/data`),
      tema escuro+dourado (QSS) espelhando o visual do dashboard antigo.
- [x] `services/tibiadata.py` e `services/wiki_images.py` portados do servidor
      Flask antigo (funcionam standalone, sem Flask/HTTP).
- [x] `services/storage.py`: persistência local em JSON, **um arquivo por
      personagem** (`data/ek_haxta.json`, `data/ms_tiomusga.json`) — resolve o
      problema encontrado no dashboard antigo, onde bestiary/bosses/charms eram
      um **estado único compartilhado**, sem separar por personagem.
- [x] Janela principal com **seletor de personagem** no topo (Haxta/EK ↔ Tio
      Musga/MS), sidebar de navegação, atualização automática a cada 3h em
      background (`QThread`) + botão "Atualizar agora" com limite de 2 min.
- [x] Aba **Personagem** funcional com dados reais ao vivo (level, mundo,
      vocação, mortes recentes, último login) + tabela Top 3 Level do Tibia.
      **Testado rodando de verdade**, confirmado por screenshot e pelo
      `data/cache_tracked.json` gerado com dados reais.
- [x] Ícone do app (`app/thoth_icon.ico`, gerado com PIL, tema preto+dourado) +
      atalho **Thoth.lnk** na área de trabalho, aponta pra `pythonw.exe` (sem
      janela de terminal) — testado, abre o app com duplo clique.
- [x] Repositório Git criado e enviado: **https://github.com/rocha5021/Toth_Controle-deProgresso**
      (branch `main`, primeiro commit com o core do app). `.gitignore` exclui
      cache de dados/estado por personagem (nada sensível versionado).
- [x] **Bosses** — view real implementada: 30 bosses portados de `_BOSS_RAW`
      (dashboard antigo), com imagem real (35/48 resolvidas via TibiaWiki,
      ver nota de taxa de acerto abaixo) e **rotação de farm por personagem**
      (botão "Marcar farmado hoje" + cooldown calculado, salvo em
      `data/<personagem>.json`). Testado (30 linhas renderizando corretamente).
- [x] **Charms** — view real implementada: 18 charms portados de `CHARMS_DB`,
      com imagem real e **checkbox de "ativo" por personagem** (salvo em
      `data/<personagem>.json`). Testado (18 linhas renderizando corretamente).
- [x] `services/image_cache.py` — cache local (`data/image_cache.json`) das
      URLs resolvidas via `wiki_images.py`, pra não bater na TibiaWiki toda
      vez que o app abre.

## 🚧 Pendente (próximos passos, na ordem que foram pedidos)

- [ ] **Hunts do EK** — motor de sugestão priorizando **lucro líquido com o
      menor gasto possível**. Hoje os dados de hunt (`_HUNT_RAW` no dashboard
      antigo) não têm campo de custo — precisa desenhar uma estimativa de custo
      (supplies) por hunt antes de calcular lucro líquido de verdade.
- [ ] **Bestiary por personagem** — Haxta e Tio Musga têm progressos diferentes;
      hoje o dado bruto (645 criaturas, `bestiary_raw.txt`) é só uma lista de
      referência, ainda não há campo de progresso por personagem. Imagens: taxa
      de acerto testada em 59/60 numa amostra — deve ir bem.
- [ ] **Quests** — tracker novo (vazio), pronto pra receber a lista que o
      usuário vai enviar com as quests **já concluídas** de Haxta e Tio Musga.
- [ ] **MS (Tio Musga)**: aba/seção específica cobrindo PvP e GvG (quando
      necessário), treino de Magic Level, e hunt em PT — item futuro, o
      usuário mencionou que ainda não faz isso hoje.
- [ ] **Bestiary/Quests já concluídos** — usuário vai enviar lista do que já
      foi feito em cada personagem, pra pré-popular o progresso em vez de
      começar do zero.
- [ ] **Armas (Club) + Equipamentos** — existiam no dashboard antigo
      (`WEAPONS_CLUB`, `EQUIPAMENTOS`), ainda não portados pro Thoth. Taxa de
      acerto de imagem testada mais baixa pra equipamentos (8/18) — os nomes
      no dashboard antigo eram estimativas, não bateram exato com a wiki;
      validar nome real por item quando formos portar.
- [ ] **Bosstiary** (Bane/Archfoe/Nemesis) — é **diferente** de "Bosses"
      (que já portamos): Bosstiary é o sistema de progressão de steps do
      próprio jogo. Existia como lista estática de 20 bosses no dashboard
      antigo (`_BOSSTIARY_RAW`/`BOSSTIARY_DB`), não portado ainda.
- [ ] **Renomear pasta `Planilha` → `Hermes`** — bloqueado: o VS Code está
      com a pasta aberta e trava o rename no Windows. Fazer quando o VS Code
      não estiver com a pasta aberta.
- [ ] Ideia mencionada pelo usuário para o futuro: gravar gameplay e cortar
      vídeos pra redes sociais — reforça que a UI deve ficar visualmente
      cuidada (tema já aplicado, mas dar atenção a polish visual conforme
      as abas forem ficando funcionais).

## 📋 Auditoria: dashboard web antigo vs Thoth (o que ainda falta portar)

Seções que existiam no dashboard web antigo e **ainda não têm equivalente**
no Thoth (nem placeholder no menu):

- **Dashboard** (visão geral/resumo) — não existe ainda no Thoth.
- **Financeiro** — controle de entradas/saídas/lucro. Fazia sentido pra 1
  personagem só; com EK+MS precisa decidir se é por personagem ou geral.
- **Upgrade Advisor** — sugestão de compra por gold disponível.
- **Wheel of Destiny** — builds recomendadas por contexto de hunt.
- **Roadmap 602-1000+** — específico do Haxta antigo (nível 602→1000+);
  precisa decidir se isso continua fazendo sentido do jeito que era.
- **Metas/Planejamento** — rotina semanal + metas diárias/semanais/mensais.
- **Checklist Diário** — lista de tarefas que reseta todo dia.
- **Transferência** — plano de migração Peloria→Inabra (Haxta); específico
  do contexto antigo, precisa validar se ainda é relevante.

Essas não foram esquecidas — ficam registradas aqui pra decidir prioridade
com o usuário antes de portar (nem tudo pode fazer sentido no formato EK+MS).

## 🗑️ Descartado / revertido

- Character Bazaar (Trade) — implementado e depois removido a pedido do usuário.
- Dashboard web em HTML/JS — não descartado, mas **substituído** como frente
  principal de desenvolvimento; arquivado em `legacy_web_dashboard/`.

## 🔗 Links e referências técnicas úteis

- TibiaData API (dados reais de personagem/mundos/highscores):
  `https://api.tibiadata.com/v4/character/<nome>`,
  `https://api.tibiadata.com/v4/worlds`,
  `https://api.tibiadata.com/v4/highscores/<mundo>/experience/all/1`
  — sem API key, mas instável às vezes (502/503 intermitente, já visto na prática).
- TibiaWiki Brasil (imagens): `https://www.tibiawiki.com.br/wiki/Especial:FilePath/<Arquivo>.gif`
  redireciona pro arquivo estático real, sem Cloudflare.
- Bazaar oficial (não usado mais, mas documentado): `https://www.tibia.com/charactertrade/`
  — atrás de Cloudflare Turnstile, só acessível via Chromium headless (Playwright).
- Repositório do Thoth: `https://github.com/rocha5021/Toth_Controle-deProgresso`

## Pastas do projeto

- `Planilha/legacy_web_dashboard/` — dashboard web antigo (HTML/CSS/JS +
  gerador Python + servidor Flask), arquivado, intacto.
- `Planilha/Thoth/` — app novo, em desenvolvimento ativo (também no GitHub).
- `Planilha/EK_Management_System.xlsx` — planilha original, na raiz.
- Pendente renomear `Planilha/` → `Hermes/` (bloqueado pelo VS Code, ver acima).
