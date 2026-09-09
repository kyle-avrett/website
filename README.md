# Kyle Avrett's website

Personal website for Kyle Avrett. The repo has two apps:

- `frontend/`: Astro site for pages, blog posts, RSS, sitemap, search, and email signup UI.
- `api/`: FastAPI service for email signup, social media notifications, and a small item CRUD route.

## Stack

- Frontend: Astro, MDX, Tailwind CSS, Pagefind, RSS, sitemap, robots.txt, Astro SEO.
- API: FastAPI, SQLAlchemy async, Alembic, PostgreSQL, listmonk, Gotify.
- Tooling: `just`, `pnpm`, `uv`, Ruff, ty, pytest, ESLint, Prettier, Vitest.

## Requirements

- Python 3.14+
- Node 22.12+
- `uv`
- `pnpm`
- `just`
- Docker, for API image build or compose preview
- PostgreSQL, for local API dev

## Setup

```sh
cp frontend/.env.example frontend/.env
cp api/.env.example api/.env
```

Frontend environment:

```sh
API_URL=http://localhost:8000
```

API environment:

```sh
APP_NAME=api
CORS_ORIGINS=https://kyleavrett.com,http://localhost:4321
LISTMONK_URL=http://localhost:9000
LISTMONK_USER=
LISTMONK_PASS=
LISTMONK_LIST=
LISTMONK_TEMPLATE_WELCOME_EMAIL=
GOTIFY_URL=
GOTIFY_TOKEN_WEBSITE=
GOTIFY_TOKEN_SOCIAL_MEDIA=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Install dependencies:

```sh
cd frontend && pnpm install
cd ../api && uv sync
```

## Run locally

From repo root:

```sh
just dev
```

That runs API and frontend dev recipes in parallel. Both recipes run their checks first.

Manual frontend:

```sh
cd frontend
pnpm dev
```

Manual API:

```sh
cd api
POSTGRES_HOST=localhost uv run alembic upgrade head
POSTGRES_HOST=localhost uv run fastapi dev src/main.py --host 0.0.0.0
```

API docs are at `http://localhost:8000/docs`. Frontend defaults to `http://localhost:4321`.

## Commands

Root recipes:

```sh
just dev      # API and frontend dev servers
just build    # API Docker build and frontend Astro build
just preview  # API Docker Compose and frontend Astro preview
just all      # setup, format, lint, typecheck, test for both apps
```

Frontend recipes:

```sh
cd frontend
just setup
just format
just lint
just typecheck
just test
just build
just preview
```

API recipes:

```sh
cd api
just setup
just format
just lint
just typecheck
just test
just make-migrations "migration name"
just migrate
just downgrade
just build
just preview
```

## Frontend

Routes live in `frontend/src/pages/`:

- `/`: home page with projects and blog posts.
- `/blog/` and `/blog/[slug]/`: content collection backed by `frontend/src/content/blog/`.
- `/projects/`: project index.
- `/projects/guidebook-studio/`: Guidebook Studio case study.
- `/work/`: resume and work history.
- `/search/`: Pagefind client search.
- `/rss.xml`: RSS feed.
- `/privacy/` and `/terms/`: legal pages.

Shared layout and UI live in `frontend/src/layouts/` and `frontend/src/components/`.

## API

FastAPI app entry point: `api/src/main.py`.

Routes mount under `/api/v1`:

- `POST /emails/subscribe`: stores an email in PostgreSQL, creates a listmonk subscriber, sends a welcome email, and sends a Gotify website notification.
- `POST /social-media/notify`: sends Gotify notifications for social media posts.
- `/item` and `/items`: small CRUD route backed by PostgreSQL.
- `GET /`: health check.

Database models live beside routes. Alembic migrations live in `api/alembic/versions/`.

## Production API

`api/docker-compose.yml` runs:

- `api`: `ghcr.io/kyle-avrett/website-api:latest`
- `database`: Postgres 18 with `database-data` volume
- `database-migrate`: one-shot `alembic upgrade head`

`.github/workflows/release.yml` runs on `master` pushes and manual dispatch:

1. API tests, Ruff, Ruff format check, and ty.
2. Docker build and push to GHCR as `latest`.
3. Deploy webhook.
4. Slack notification.
