# PRD - Diablo 2 Resurrected Magic Find Run Tracker

## Visão Geral

Aplicação web para rastrear e contabilizar runs de Magic Find no Diablo 2 Resurrected, permitindo ao jogador cronometrar cada run, registrar itens encontrados e analisar estatísticas por local e perfil de jogo.

---

## Problema

Jogadores de D2R que fazem farming de MF não têm uma forma organizada de rastrear quantas runs fizeram, quanto tempo gastaram e quais itens encontraram em cada local. Isso dificulta a análise de eficiência e a tomada de decisão sobre onde farmar.

---

## Personas

- **Jogador MF casual**: quer registrar seus drops para compartilhar ou lembrar.
- **Jogador MF dedicado**: quer analisar eficiência por local, tempo médio de run e taxa de drops valiosos.
- **Multi-perfil**: joga em diferentes modos (solo, online, ladder, non-ladder, hardcore) e quer separar estatísticas.

---

## Funcionalidades

### 1. Gerenciamento de Perfis

| Campo | Descrição |
|-------|-----------|
| Nome do perfil | Identificador livre (ex: "Sorceress Ladder S14", "Warlock RoTW HC", "Hammerdin NL") |
| Modo de jogo | Ladder / Non-Ladder / Hardcore / Hardcore Ladder |
| Classe | Amazon, Necromancer, Barbarian, Sorceress, Paladin, Druid, Assassin, **Warlock** [RoTW] |

- O usuário pode criar múltiplos perfis.
- Todas as runs são vinculadas a um perfil ativo.
- Troca de perfil disponível a qualquer momento (fora de uma run ativa).

### 2. Timer de Run

| Ação | Comportamento |
|------|---------------|
| **Start** | Inicia o cronômetro. O usuário deve selecionar o local antes de iniciar. |
| **Pause** | Pausa o cronômetro. Pode ser retomado. |
| **Resume** | Retoma o cronômetro após pausa. |
| **Finish** | Para o cronômetro, registra o tempo total e abre o formulário de registro de itens. |

- O timer deve mostrar minutos e segundos (MM:SS) em tempo real.
- O tempo registrado desconta pausas (tempo líquido de run).

### 3. Seleção de Local (Área de Farm)

Locais disponíveis para seleção antes de iniciar a run:

| Local | Ato | Notas |
|-------|-----|-------|
| Andariel | Ato 1 | |
| Countess | Ato 1 | |
| Pit | Ato 1 | |
| Cows | Ato 1 | |
| Stony Tombs | Ato 2 | |
| Arcane Sanctuary | Ato 2 | |
| Ancient Tunnels | Ato 2 | |
| Lower Kurast | Ato 3 | |
| Travincal | Ato 3 | |
| Mephisto | Ato 3 | |
| Chaos Sanctuary | Ato 4 | |
| Eldritch & Shenk | Ato 5 | |
| Pindleskin | Ato 5 | |
| Worldstone Keep | Ato 5 | |
| Terror Zone (rotativa) | Variável | [RoTW] Rotação a cada 30 min |
| Colossal Ancients | Especial | [RoTW] Encounter pinnacle via portal vermelho |

- O contador de runs é incrementado por local (Run #1 no Pit, Run #5 em Mephisto, etc.).
- Cada local mantém seu próprio sequencial dentro do perfil.

### 4. Registro de Itens (pós-Finish)

Ao finalizar a run, o sistema apresenta um formulário para registrar itens encontrados:

- **ComboBox com busca** (autocomplete/filtro por texto digitado).
- Permite inserir **múltiplos itens** por run.
- Cada item adicionado aparece em uma lista editável (pode remover antes de confirmar).
- Botão **"Salvar Run"** confirma o registro.
- Botão **"Nenhum item"** / "Pular" permite registrar run sem drops relevantes.

#### 4.1 Categorias de Itens na ComboBox

A combobox deve conter todos os itens agrupados por categoria, incluindo todo conteúdo até a versão 3.2 (Reign of the Warlock):

**A) Itens Base (para Runewords)**
- Todas as armaduras, helmos, escudos e armas que servem como base para runewords.
- Variantes: Normal, Superior, Ethereal, Superior Ethereal.
- Exemplos clássicos: Monarch, Archon Plate, Dusk Shroud, Berserker Axe, Phase Blade, Flail, Crystal Sword, Thresher, Giant Thresher, Colossus Voulge, etc.
- **[RoTW] Grimoires** (off-hand exclusivo do Warlock, servem como base para runewords como Vigilance):
  - Normal: Old Book, Tome, Codex, Compendium, Grimoire
  - Exceptional: Burnt Text, Dark Tome, Dark Codex, Possessed Compendium, Possessed Grimoire
  - Elite: Forgotten Volume, Occult Tome, Occult Codex, Blasphemous Compendium, Blasphemous Grimoire
- **[RoTW] Daggers** (agora podem ter staff mods de Warlock, servem como base para runewords Void e Ritual):
  - Mithril Point, Fanged Knife, Legend Spike, etc.

**B) Itens Mágicos e Raros valiosos**
- Botas (Mágicas/Raras)
- Luvas (Mágicas/Raras)
- Diadems
- Tiaras
- Circlets
- Coronets
- Escudos (Mágicos/Raros)
- Armaduras (Mágicas/Raras)
- Anéis (Mágicos/Raros)
- Amuletos (Mágicos/Raros)
- Cintos (Mágicos/Raros)
- Javelins (Mágicas/Raras - ex: Matriarchal Javelin)
- Cetros (Mágicos/Raros)
- Varinhas/Wands (Mágicas/Raras)
- Claws (Assassin - Mágicas/Raras)
- **[RoTW] Grimoires Mágicos/Raros** (com staff mods de Warlock, FCR, -enemy magic res)
- **[RoTW] Daggers Mágicos/Raros** (com +1-3 Warlock skills)

**C) Charms**
- Small Charms (valiosos: life/mana, resistências, MF, FHR, poison damage)
- Grand Charms (valiosos: skillers +1 skill tree, life, FHR)
- Annihilus (Unique Small Charm)
- Hellfire Torch (Unique Large Charm)
- Gheed's Fortune (Unique Grand Charm)
- **[RoTW] Sunder Charms (Renewed)** — versões melhoradas com stats aleatórios adicionais:
  - Renewed Rotting Fissure (Poison)
  - Renewed Cold Rupture (Cold)
  - Renewed Crack of the Heavens (Lightning)
  - Renewed Flame Rift (Fire)
  - Renewed Bone Break (Physical)
  - Renewed Black Cleft (Magic)
- Sunder Charms (Latent) — versões base que dropam de Heralds em Terror Zones:
  - Latent Rotting Fissure
  - Latent Cold Rupture
  - Latent Crack of the Heavens
  - Latent Flame Rift
  - Latent Bone Break
  - Latent Black Cleft

**D) Jewels**
- Jewels Mágicas valiosas (ED/IAS, ED/min damage, resistências, facets)
- Rainbow Facets (todas as variantes: fire/cold/light/poison, die/level-up)
- **[RoTW] Colossal Ancient Jewels** (unique jewels do encounter pinnacle, req level 75, limitada a 1 por personagem):
  - Defender's Bile (Poison: +poison skill damage, -enemy poison res, MF, XP)
  - Guardian's Thunder (Lightning: +lightning skill damage, -enemy lightning res, MF, XP)
  - Protector's Frost (Cold: +cold skill damage, -enemy cold res, MF, XP)
  - Defender's Fire (Fire: +fire skill damage, -enemy fire res, MF, XP)
  - Protector's Stone (Physical: +enhanced damage, -enemy physical res, MF, XP)
  - Guardian's Light (Magic: +magic skill damage, -enemy magic res, MF, XP)

**E) Set Items (todos)**
Lista completa de todos os set items do jogo, organizados por set:

*Sets Clássicos (LoD):*
- Aldur's Watchtower
- Angelic Raiment
- Arcanna's Tricks
- Arctic Gear
- Bul-Kathos' Children
- Cathan's Traps
- Cow King's Leathers
- Death's Disguise
- Griswold's Legacy
- Hwanin's Majesty
- Immortal King
- Infernal Tools
- Iratha's Finery
- M'avina's Battle Hymn
- Milabrega's Regalia
- Naj's Ancient Vestige
- Natalya's Odium
- Orphan's Call
- Sander's Folly
- Sazabi's Grand Tribute
- Sigon's Complete Steel
- Tal Rasha's Wrappings
- Tancred's Battlegear
- Telling of Beads
- The Disciple
- Trang-Oul's Avatar
- Vidala's Rig
- (todos os demais)

*[RoTW] Novos Sets (Patch 3.0+):*
- **Horazon's Splendor** (Elite Warlock set, 5 peças):
  - Horazon's Countenance (Demonhead)
  - Horazon's Dominion (Russet Armor)
  - Horazon's Hold (Demonhide Gloves)
  - Horazon's Legacy (Mirrored Boots)
  - Horazon's Secrets (Occult Codex / Grimoire)
- **Bane's Garments** (Normal set, 3 peças, todas as classes):
  - Bane's Wraithskin (Hard Leather Armor)
  - Bane's Authority (Light Belt)
  - Bane's Oathmaker (Kris)

**F) Itens Únicos (todos)**
Todos os unique items do jogo, de todas as categorias:

*Clássicos (LoD):*
- Helmos únicos (Shako/Harlequin Crest, Crown of Ages, Griffon's Eye, Nightwing's Veil, etc.)
- Armaduras únicas (Skullder's Ire, Vipermagi, Que-Hegan's Wisdom, etc.)
- Armas únicas (Death's Fathom, Windforce, Grandfather, etc.)
- Escudos únicos (Stormshield, Herald of Zakarum, Homunculus, etc.)
- Botas únicas (War Traveler, Sandstorm Trek, Marrowwalk, etc.)
- Luvas únicas (Chance Guards, Magefist, Frostburn, etc.)
- Cintos únicos (Arachnid Mesh, Verdungo's, String of Ears, Thundergod's, etc.)
- Anéis únicos (Stone of Jordan, Bul-Kathos' Wedding Band, Nature's Peace, Wisp Projector, Dwarf Star, Raven Frost, etc.)
- Amuletos únicos (Mara's Kaleidoscope, Highlord's Wrath, Tal Rasha's Adjudication, Metalgrid, Seraph's Hymn, etc.)
- Todas as demais categorias

*[RoTW] Novos Únicos (Patch 3.0+):*
- **Grimoires Únicos:**
  - Ars Al'Diabolos (Blasphemous Grimoire) — +2 Chaos Skills, FCR, fire skill damage, -enemy fire res
  - Ars Tor'Baalos (Blasphemous Compendium) — +2 Demon Skills, life scaling, physical damage reduction
  - Ars Dul'Mephistos (Occult Tome) — +2 Warlock Skills, FCR, FHR, -enemy magic resistance, MF
  - Measured Wrath (Burnt Text) — +1 Warlock Skills, FCR, mid-game progression
- **Armas Únicas:**
  - Dreadfang (Legend Sword) — Amplify Damage proc, IAS, ED, Deadly Strike, +3 Mirrored Blades
  - Bloodpact Shard (Mithril Point) — +1 All Skills, FCR, +life%, Warlock skill bonuses, MF
- **Botas Únicas:**
  - Wraithstep (Mirrored Boots) — FRW, FHR, +Warlock skill tree, Dex/Energy
- **Helmos Únicos:**
  - Hellwarden's Will (Death Mask) — +1 All Skills, IAS, FCR, -enemy fire/magic res
- **Cintos Únicos:**
  - Gheed's Wager (Troll Belt) — FCR, FHR, FRW, -enemy magic res, All Res, Extra Gold
- **Amuletos Únicos:**
  - Entropy Locket — magic skill damage, FCR, Miasma Chain proc, Lightning Res, Max Mana%
- **Anéis Únicos:**
  - Sling — FCR, -enemy magic res, Town Portal charges, Slow Target, MF
  - Opalvein — Flame Wave proc, FCR, All Res, life/mana after kill

**G) Runewords**
Todas as runewords do jogo, incluindo as novas:

*[RoTW] Novas Runewords (Patch 3.0+):*
- **Authority** (Hel + Shael + Ral) — 3os Body Armor — +2 Warlock Skills, FHR, ED, Miasma Chain proc
- **Coven** (Ist + Ral + Io) — 3os Helm — +1 All Skills, FCR, MF, Fire Res
- **Void** (Thul + Zod + Ist) — 3os Dagger — +2 All Skills, FCR, Magic Skill Damage, Indestructible, MF
- **Vigilance** (Dol + Gul) — 2os Grimoire/Shield/Voodoo Head/Auric Shield — FRW, FBR, Life, Mana, All Res
- **Ritual** (Amn + Shael + Ohm) — 3os Dagger — IAS, ED, Damage to Demons, Life Leech

*[RoTW] Ladder-only Runewords:*
- **Hysteria** (Shael + Ko + Eld) — 3os Body Armor — FRW, IAS, FHR, +Evade, Dex, All Res
- **Mania** (Shael + Ko + Eld) — 3os Weapons — Burst of Speed proc, Level 1 Fanaticism Aura, IAS, ED

*Nota: Todas as runewords clássicas e de patches anteriores (2.4-2.6) também devem estar listadas.*

**H) Runas (todas)**
- El → Zod (todas as 33 runas, listadas em ordem)
- El, Eld, Tir, Nef, Eth, Ith, Tal, Ral, Ort, Thul, Amn, Sol, Shael, Dol, Hel, Io, Lum, Ko, Fal, Lem, Pul, Um, Mal, Ist, Gul, Vex, Ohm, Lo, Sur, Ber, Jah, Cham, Zod

**I) [RoTW] Consumíveis e Materiais**
- **Worldstone Shards** (usados para terrorizar Atos inteiros e em receitas de Sunder):
  - Western Worldstone Shard (Ato 1)
  - Eastern Worldstone Shard (Ato 2)
  - Southern Worldstone Shard (Ato 3)
  - Deep Worldstone Shard (Ato 4)
  - Northern Worldstone Shard (Ato 5)
- **Colossal Ancient Statues** (combinadas no Cubo para abrir portal do encounter pinnacle):
  - Talic's Anguish
  - Korlic's Pain
  - Madawc's Ire
  - Bul-Kathos' Nightmare
  - Worusk's End

### 5. Lista/Histórico de Runs

Cada run registrada deve exibir:

| Campo | Descrição |
|-------|-----------|
| # | Número sequencial da run naquele local |
| Local | Área onde a run foi feita |
| Tempo | Duração da run (MM:SS) |
| Itens | Lista de itens encontrados (ou "Nenhum") |
| Data/Hora | Timestamp do registro |

- Filtro por local.
- Filtro por perfil (automático pelo perfil ativo).
- Ordenação por data (mais recente primeiro).

### 6. Estatísticas (nice-to-have v1.1)

- Total de runs por local.
- Tempo médio por run por local.
- Itens encontrados por local (frequência).
- Tempo total investido por local.

---

## Requisitos Não-Funcionais

| Requisito | Detalhe |
|-----------|---------|
| Persistência | Dados salvos em localStorage ou IndexedDB (sem backend inicialmente) |
| Responsividade | Funcionar bem em desktop (uso primário ao lado do jogo) |
| Performance | Timer preciso, UI responsiva mesmo com muitas runs registradas |
| Exportação | Possibilidade de exportar dados em JSON (backup/restore) |

---

## Stack Técnica (sugestão)

| Camada | Tecnologia |
|--------|------------|
| Frontend | React + TypeScript |
| UI | Tailwind CSS |
| State | Zustand ou Context API |
| Persistência | localStorage / IndexedDB |
| ComboBox | React Select ou similar com busca |
| Build | Vite |

---

## User Flow Principal

```
1. Usuário seleciona/cria perfil
2. Seleciona o local da run
3. Clica "Start" → timer inicia
4. (Opcional) Pausa/Resume durante a run
5. Clica "Finish" → timer para
6. Sistema mostra formulário de itens:
   - ComboBox com busca para adicionar itens
   - Pode adicionar múltiplos itens
   - Pode pular se não encontrou nada
7. Clica "Salvar Run"
8. Run aparece no histórico com #, tempo e itens
9. Contador do local é incrementado
```

---

## Escopo v1.0 (MVP)

- [x] CRUD de perfis
- [x] Timer com start/pause/resume/finish
- [x] Seleção de local
- [x] Registro de itens via combobox com busca
- [x] Histórico de runs por perfil e local
- [x] Persistência local
- [x] Export/Import JSON

## Escopo v1.1

- [ ] Estatísticas e gráficos
- [ ] Filtros avançados no histórico
- [ ] Tema dark/light
- [ ] PWA (uso offline garantido)

---

## Wireframe Conceitual

```
┌─────────────────────────────────────────────────┐
│  [Perfil: Sorceress Ladder ▼]                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  Local: [Mephisto ▼]     Run #47               │
│                                                 │
│         ┌──────────┐                            │
│         │  03:42   │  ← Timer                   │
│         └──────────┘                            │
│                                                 │
│  [ Start ]  [ Pause ]  [ Finish ]               │
│                                                 │
├─────────────────────────────────────────────────┤
│  Histórico - Mephisto                           │
│                                                 │
│  #47 | 03:42 | Shako, Ist Rune       | 14:32   │
│  #46 | 02:58 | Nenhum                 | 14:28   │
│  #45 | 03:15 | War Traveler           | 14:25   │
│  ...                                            │
└─────────────────────────────────────────────────┘
```

---

## Considerações

- A lista de itens na combobox deve ser pré-carregada e estática (dados do jogo não mudam entre patches).
- Os itens devem ter tags/categorias para facilitar a busca (ex: digitar "shako" encontra "Harlequin Crest (Shako)").
- O banco de itens pode ser um arquivo JSON separado para fácil manutenção.
- Considerar aliases populares (ex: "HoZ" → Herald of Zakarum, "Arach" → Arachnid Mesh, "Void" → Void Runeword).
- **[RoTW]** Itens devem ter uma tag indicando se são conteúdo novo (Patch 3.0+) para facilitar filtragem.
- **[RoTW]** Considerar que Grimoires são exclusivos do Warlock — na busca, exibir essa informação.
- **[RoTW]** Runewords ladder-only (Hysteria, Mania) devem ser marcadas como tal.
- **[RoTW]** Terror Zones rotam a cada 30 minutos — considerar campo opcional para anotar qual TZ estava ativa.
- **[RoTW]** Colossal Ancient Jewels são limitadas a 1 por personagem — informação útil para o jogador ao registrar.
- A base de itens deve cobrir todo conteúdo de D2R v1.0 até v3.2 (Reign of the Warlock, Season 14).
