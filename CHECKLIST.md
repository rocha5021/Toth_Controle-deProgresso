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
- [x] Abas Hunts/Bosses/Bestiary/Charms/Quests existem no menu com uma tela
      "em construção" (para não fingir que já funcionam).

## 🚧 Pendente (próximos passos, na ordem que foram pedidos)

- [ ] **Hunts do EK** — motor de sugestão priorizando **lucro líquido com o
      menor gasto possível**. Hoje os dados de hunt (`_HUNT_RAW` no dashboard
      antigo) não têm campo de custo — precisa desenhar uma estimativa de custo
      (supplies) por hunt antes de calcular lucro líquido de verdade.
- [ ] **Rotação de bosses do EK** — portar o controle de cooldown/farm (existia
      no dashboard antigo como `ek_boss_farm`, mas era compartilhado — agora
      precisa ser por personagem, usando `storage.py`).
- [ ] **Bestiary por personagem** — Haxta e Tio Musga têm progressos diferentes;
      hoje o dado bruto (645 criaturas, `bestiary_raw.txt`) é só uma lista de
      referência, ainda não há campo de progresso por personagem.
- [ ] **Charms** — referência + seleção ativa por personagem.
- [ ] **Quests** — tracker novo (vazio), pronto pra receber a lista que o
      usuário vai enviar com as quests **já concluídas** de Haxta e Tio Musga.
- [ ] **MS (Tio Musga)**: aba/seção específica cobrindo PvP e GvG (quando
      necessário), treino de Magic Level, e hunt em PT — item futuro, o
      usuário mencionou que ainda não faz isso hoje.
- [ ] **Bestiary já concluído** — usuário vai enviar lista do que já foi feito
      em cada personagem, pra pré-popular o progresso em vez de começar do zero.
- [ ] **Cyclopedia com imagens reais** (retomar) — usar a técnica
      `Especial:FilePath` já validada para trazer imagens de itens/criaturas/
      charms/bosses reais na interface, sem precisar baixar nada.
- [ ] Ideia mencionada pelo usuário para o futuro: gravar gameplay e cortar
      vídeos pra redes sociais — reforça que a UI deve ficar visualmente
      cuidada (tema já aplicado, mas dar atenção a polish visual conforme
      as abas forem ficando funcionais).

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

## Pastas do projeto

- `Planilha/legacy_web_dashboard/` — dashboard web antigo (HTML/CSS/JS +
  gerador Python + servidor Flask), arquivado, intacto.
- `Planilha/Thoth/` — app novo, em desenvolvimento ativo.
- `Planilha/EK_Management_System.xlsx` — planilha original, na raiz.
