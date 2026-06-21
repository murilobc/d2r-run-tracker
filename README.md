# 🎮 D2R Magic Find Run Tracker

Aplicação para rastrear runs de Magic Find no Diablo 2 Resurrected (v3.2 - Reign of the Warlock).

## Features

- ⏱️ Timer com start/pause/resume/finish (tempo líquido)
- 📍 16 locais de farm (incluindo Terror Zones e Colossal Ancients)
- 🔍 Busca de itens com aliases (359 itens, incluindo conteúdo RoTW)
- 👤 Múltiplos perfis (8 classes, 4 modos de jogo)
- 📋 Histórico com filtros por local
- 📊 Estatísticas (runs/local, tempo médio, top drops)
- 💾 Export/Import JSON

## Quick Start

```bash
cp .env.example .env
docker compose up -d
```

Acesse:
- **Frontend:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs

> Se as portas estiverem em uso, ajuste `API_PORT` e `FRONTEND_PORT` no `.env`.

## Primeiro uso

1. Acesse a página **Perfis** e crie um perfil
2. Selecione o perfil criado como ativo
3. Vá para **Run Tracker**, escolha o local e clique Start
4. Ao finalizar, registre os itens encontrados
5. Consulte o **Histórico** e **Estatísticas**

## Stack

| Camada | Tecnologia |
|--------|-----------|
| API | Python 3.12, FastAPI, SQLAlchemy 2.0, asyncpg |
| Frontend | Streamlit |
| DB | PostgreSQL 16 |
| Infra | Docker, Docker Compose |

## Desenvolvimento

```bash
# Rodar testes
docker compose up -d db
docker compose run --rm api pytest tests/ -v

# Rodar migration
docker compose run --rm api alembic -c alembic.ini upgrade head

# Rebuild após mudanças
docker compose build
docker compose up -d
```

## Estrutura

```
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routers/         # API endpoints
│   │   └── seed/            # Item database (359 items)
│   ├── alembic/             # Migrations
│   └── tests/               # 18 tests
├── frontend/
│   ├── app.py               # Streamlit entry
│   ├── pages/               # UI pages
│   └── api_client.py        # HTTP client
├── docker-compose.yml
├── Dockerfile.api
└── Dockerfile.frontend
```

## Licença

Projeto pessoal. Diablo 2 Resurrected é propriedade da Blizzard Entertainment.
