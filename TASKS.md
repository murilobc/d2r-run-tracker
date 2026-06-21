# Plano de Tarefas — D2R MF Run Tracker

## Stack Definida

| Camada | Tecnologia |
|--------|------------|
| Backend API | Python 3.12 + FastAPI |
| Frontend | Python + Streamlit |
| Banco de Dados | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 + Alembic (migrations) |
| Validação | Pydantic v2 |
| Containerização | Docker + Docker Compose |
| Testes | pytest + httpx (API) |

**Justificativa do PostgreSQL:** dados relacionais (perfis → runs → itens), queries com filtros e agregações (estatísticas), suporte a JSON para flexibilidade futura, e excelente performance com índices para buscas na tabela de itens. SQLite seria insuficiente para deploy online multi-usuário.

---

## Estrutura do Projeto

```
d2r-run-tracker/
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.frontend
├── .env.example
├── backend/
│   ├── alembic/
│   │   ├── alembic.ini
│   │   └── versions/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings (pydantic-settings)
│   │   ├── database.py          # Engine, session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── profile.py
│   │   │   ├── run.py
│   │   │   └── item.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── profile.py
│   │   │   ├── run.py
│   │   │   └── item.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── profiles.py
│   │   │   ├── runs.py
│   │   │   ├── items.py
│   │   │   └── export.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── profile_service.py
│   │   │   └── run_service.py
│   │   └── seed/
│   │       ├── __init__.py
│   │       ├── seed_items.py    # Script de seed
│   │       └── items_data.json  # Base completa de itens D2R v3.2
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_profiles.py
│   │   ├── test_runs.py
│   │   └── test_items.py
│   └── requirements.txt
├── frontend/
│   ├── app.py                   # Entry point Streamlit
│   ├── pages/
│   │   ├── 1_🎮_Run_Tracker.py
│   │   ├── 2_📋_Histórico.py
│   │   ├── 3_👤_Perfis.py
│   │   └── 4_📊_Estatísticas.py
│   ├── components/
│   │   ├── timer.py
│   │   ├── item_selector.py
│   │   └── run_list.py
│   ├── api_client.py            # Wrapper HTTP para o backend
│   └── requirements.txt
└── README.md
```

---

## Fases e Tarefas

### Fase 0 — Infraestrutura (Docker + Projeto Base)

| # | Tarefa | Descrição |
|---|--------|-----------|
| 0.1 | `docker-compose.yml` | Serviços: `db` (postgres), `api` (fastapi), `frontend` (streamlit). Rede interna, volumes para persistência do DB. |
| 0.2 | `Dockerfile.api` | Python 3.12-slim, instala requirements, expõe porta 8000, CMD uvicorn. |
| 0.3 | `Dockerfile.frontend` | Python 3.12-slim, instala requirements, expõe porta 8501, CMD streamlit run. |
| 0.4 | `.env.example` | DATABASE_URL, API_URL, POSTGRES_USER/PASSWORD/DB. |
| 0.5 | Backend base | `main.py` com FastAPI app, CORS, lifespan. `config.py` com pydantic-settings. `database.py` com async engine + sessionmaker. |
| 0.6 | Alembic setup | Init alembic, configurar `env.py` para usar models do projeto. |

---

### Fase 1 — Modelagem e Banco de Dados

| # | Tarefa | Descrição |
|---|--------|-----------|
| 1.1 | Model `Profile` | `id`, `name`, `game_mode` (enum: ladder/non-ladder/hardcore/hc-ladder), `character_class` (enum com 8 classes incluindo Warlock), `created_at`. |
| 1.2 | Model `Item` | `id`, `name`, `category` (enum: base/magic_rare/charm/jewel/set/unique/runeword/rune/consumable), `subcategory` (text), `aliases` (array text), `is_rotw` (bool), `is_ladder_only` (bool). Tabela estática, seed-only. |
| 1.3 | Model `Run` | `id`, `profile_id` (FK), `location` (enum dos 16 locais), `run_number` (int, sequencial por profile+location), `duration_seconds` (int), `terror_zone_note` (text, opcional), `created_at`. |
| 1.4 | Model `RunItem` | `id`, `run_id` (FK), `item_id` (FK). Tabela associativa N:N. |
| 1.5 | Migration inicial | Gerar migration com Alembic para criar todas as tabelas. |
| 1.6 | Índices | Index em `(profile_id, location)` na tabela runs. Index em `name` e `aliases` na tabela items (para busca). |

---

### Fase 2 — Seed de Itens (Base de Dados D2R v3.2)

| # | Tarefa | Descrição |
|---|--------|-----------|
| 2.1 | Estrutura `items_data.json` | JSON com array de objetos: `{name, category, subcategory, aliases[], is_rotw, is_ladder_only}`. |
| 2.2 | Runas | Todas as 33 runas (El → Zod). |
| 2.3 | Itens Únicos clássicos | Todos os uniques LoD (~400 itens) organizados por tipo. |
| 2.4 | Itens Únicos RoTW | 12 novos (4 grimoires + Dreadfang, Bloodpact Shard, Wraithstep, Hellwarden's Will, Gheed's Wager, Entropy Locket, Sling, Opalvein). |
| 2.5 | Set Items clássicos | Todos os set items LoD (~127 peças). |
| 2.6 | Set Items RoTW | Horazon's Splendor (5 peças) + Bane's Garments (3 peças). |
| 2.7 | Runewords | Todas as runewords clássicas + patches 2.4-2.6 + RoTW (Authority, Coven, Void, Vigilance, Ritual, Hysteria, Mania). |
| 2.8 | Itens Base | Bases valiosas para runewords (armaduras, escudos, armas elite) + Grimoires (15 bases). |
| 2.9 | Charms | Small/Grand Charms genéricos valiosos, Annihilus, Torch, Gheed's, Sunder Charms (Latent + Renewed, 12 total). |
| 2.10 | Jewels | Rainbow Facets (8 variantes) + Colossal Ancient Jewels (6) + Jewels genéricas valiosas. |
| 2.11 | Mágicos/Raros | Categorias genéricas (Rare Boots, Magic Amulet, Rare Circlet, etc.) — representados como tipos, não itens individuais. |
| 2.12 | Consumíveis RoTW | Worldstone Shards (5) + Colossal Ancient Statues (5). |
| 2.13 | Script `seed_items.py` | Lê JSON, faz upsert na tabela items. Executado no startup ou via comando. |

---

### Fase 3 — API Backend (Routers + Services)

| # | Tarefa | Descrição |
|---|--------|-----------|
| 3.1 | Router `profiles` | `POST /profiles`, `GET /profiles`, `GET /profiles/{id}`, `PUT /profiles/{id}`, `DELETE /profiles/{id}`. |
| 3.2 | Router `items` | `GET /items?search=&category=&limit=50` — busca com ILIKE em name e aliases, filtro por categoria. |
| 3.3 | Router `runs` | `POST /runs` (cria run com duration, location, profile_id, item_ids[]), `GET /runs?profile_id=&location=&page=&size=`, `DELETE /runs/{id}`. |
| 3.4 | Lógica `run_number` | No service, calcular próximo sequencial: `SELECT MAX(run_number) FROM runs WHERE profile_id=X AND location=Y`. |
| 3.5 | Router `export` | `GET /export/{profile_id}` — retorna JSON completo. `POST /import` — recebe JSON e reconstrói dados. |
| 3.6 | Schemas Pydantic | Request/Response models para cada endpoint. Validação de enums. |
| 3.7 | Error handling | Exception handlers globais. Respostas padronizadas 4xx/5xx. |

---

### Fase 4 — Frontend Streamlit

| # | Tarefa | Descrição |
|---|--------|-----------|
| 4.1 | `api_client.py` | Classe com métodos para cada endpoint da API (usa `httpx`). |
| 4.2 | Página Perfis | CRUD de perfis. Seleção do perfil ativo (session_state). Form de criação com nome, modo de jogo, classe. |
| 4.3 | Componente Timer | Timer visual MM:SS com `st.empty()` + loop. Botões Start/Pause/Resume/Finish. Lógica de tempo líquido (desconta pausas). Usa `session_state` para estado. |
| 4.4 | Página Run Tracker | Seletor de local (selectbox). Exibe "Run #N" (próximo sequencial). Timer integrado. Ao Finish → abre formulário de itens. |
| 4.5 | Componente Item Selector | `st.selectbox` com busca (ou `st_searchbox`/componente custom). Chamada à API `/items?search=`. Lista de itens adicionados com botão remover. Botões "Salvar Run" e "Nenhum item". |
| 4.6 | Página Histórico | Tabela com runs do perfil ativo. Filtro por local. Colunas: #, Local, Tempo, Itens, Data. Ordenação mais recente primeiro. |
| 4.7 | Página Estatísticas | Total runs por local (bar chart). Tempo médio por local. Top itens encontrados (frequência). Tempo total investido. |
| 4.8 | Export/Import | Botão download JSON (perfil completo). Upload JSON para importar. |
| 4.9 | Sidebar | Perfil ativo exibido. Link para troca de perfil. Navegação entre páginas. |

---

### Fase 5 — Testes

| # | Tarefa | Descrição |
|---|--------|-----------|
| 5.1 | Fixtures | DB de teste (SQLite in-memory ou postgres de teste), client httpx AsyncClient. |
| 5.2 | Testes Profiles | CRUD completo, validação de enums inválidos. |
| 5.3 | Testes Runs | Criar run, verificar run_number sequencial, filtros por location/profile. |
| 5.4 | Testes Items | Busca por nome, busca por alias, filtro por categoria, paginação. |
| 5.5 | Teste Export/Import | Exportar perfil, importar em perfil novo, verificar integridade. |

---

### Fase 6 — Polish e Deploy

| # | Tarefa | Descrição |
|---|--------|-----------|
| 6.1 | README.md | Instruções de setup local (`docker compose up`), variáveis de ambiente, screenshots. |
| 6.2 | Healthcheck | Endpoint `/health` na API. Healthcheck no docker-compose para db e api. |
| 6.3 | Tema Diablo | CSS custom no Streamlit (dark theme, cores temáticas). |
| 6.4 | Produção | docker-compose.prod.yml com restart policies, limites de memória, env vars seguras. |
| 6.5 | Seed automático | No lifespan do FastAPI, rodar seed se tabela items estiver vazia. |

---

## Ordem de Execução Recomendada

```
Fase 0 (infra)
    → Fase 1 (models + migrations)
        → Fase 2 (seed de itens)
            → Fase 3 (API)
                → Fase 4 (frontend)
                    → Fase 5 (testes)
                        → Fase 6 (polish)
```

As fases 2 e 3 podem ter trabalho parcialmente paralelo (seed pode ser refinado enquanto a API básica já funciona).

---

## Decisões Técnicas

| Decisão | Justificativa |
|---------|---------------|
| PostgreSQL vs SQLite | Multi-usuário, queries complexas, deploy online. SQLite limita concorrência. |
| SQLAlchemy 2.0 async | Performance em I/O, padrão moderno FastAPI. |
| Streamlit vs outro frontend | Requisito do projeto. Limitação: timer em real-time precisa de workaround com `st.empty()` + rerun. |
| Items como tabela estática | Dados do jogo não mudam. Seed uma vez, busca rápida com índice. Evita JSON gigante no frontend. |
| Aliases no banco | Permite buscar "shako" e encontrar "Harlequin Crest". ILIKE em array ou campo text searchable. |
| Docker multi-stage | Imagens menores, build separado de runtime. |

---

## Estimativa de Esforço

| Fase | Estimativa |
|------|-----------|
| Fase 0 | 2-3h |
| Fase 1 | 2-3h |
| Fase 2 | 4-6h (maior parte é curadoria do JSON de itens) |
| Fase 3 | 4-5h |
| Fase 4 | 6-8h (timer é o ponto mais complexo no Streamlit) |
| Fase 5 | 3-4h |
| Fase 6 | 2-3h |
| **Total** | **~23-32h** |
