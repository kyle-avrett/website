# Kyle Avrett's website

Personal website for Kyle Avrett. Repo has two apps:

- `frontend/`: Astro site for static pages, MDX content collections, RSS, sitemap, Pagefind search, SEO metadata, and email signup UI.
- `api/`: FastAPI service for email signup, social media notifications, outbound webhooks, generated MCP tools, and a small item CRUD route.

## Stack

- Frontend: Astro, MDX, Tailwind CSS, Cloudflare adapter, Astro Icon, Pagefind, RSS, sitemap, robots.txt, Astro SEO, `llms.txt`.
- API: FastAPI, FastMCP, FastMCP docs, SQLAlchemy async, Alembic, PostgreSQL, listmonk, Gotify.
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
BASE_URL=http://localhost:8000
CORS_ORIGINS=https://kyleavrett.com,http://localhost:4321
LISTMONK_URL=http://localhost:9000
LISTMONK_USER=
LISTMONK_PASS=
LISTMONK_LIST=
LISTMONK_TEMPLATE_WELCOME_EMAIL=
GOTIFY_URL=
GOTIFY_TOKEN_WEBSITE=
GOTIFY_TOKEN_SOCIAL_MEDIA=
WEBHOOK_URLS=
WEBHOOK_SECRET=
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

That runs API and frontend dev recipes in parallel. Both recipes run `all` first, so setup, format, lint, typecheck, and test run before servers start.

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

Docs index is at `http://localhost:8000/docs`. API docs are at `/docs/api`. MCP docs are at `/docs/mcp`. MCP endpoint is `http://localhost:8000/mcp`. Frontend defaults to `http://localhost:4321`.

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

Astro routes live in `frontend/src/pages/`:

- `/`: home page with overview, project cards, blog cards, and newsletter signup.
- `/blog/`: blog index backed by `frontend/src/content/blog/`.
- `/blog/[slug]/`: non-draft blog posts from the blog content collection.
- `/projects/`: project index backed by `frontend/src/content/projects/`.
- `/projects/[slug]/`: non-draft project case studies from the project content collection.
- `/work/`: resume and work history.
- `/search/`: Pagefind client search.
- `/rss.xml`: RSS feed for non-draft blog posts.
- `/privacy/` and `/terms/`: legal pages.

Shared layout and UI live in `frontend/src/layouts/` and `frontend/src/components/`.

## API

FastAPI app entry point: `api/src/main.py`.

REST routes:

- `GET /`: health check.
- `POST /api/v1/emails/subscribe`: stores an email in PostgreSQL, creates a listmonk subscriber, sends a welcome email, sends a Gotify website notification, and emits `email.subscribed` webhooks when configured.
- `POST /api/v1/social-media/notify`: sends Gotify notifications for social media posts and emits `social_media.published` webhooks when configured.
- `POST /api/v1/item`, `GET /api/v1/item/{item_id}`, `PUT /api/v1/item/{item_id}`, `DELETE /api/v1/item/{item_id}`, and `GET /api/v1/items`: small CRUD route backed by PostgreSQL.

Database models live beside routes. Alembic migrations live in `api/alembic/versions/`.

Docs and MCP routes:

- `/docs`: docs index.
- `/docs/api`: FastAPI Swagger UI.
- `/docs/api/redoc`: FastAPI ReDoc.
- `/docs/api/openapi.json`: FastAPI OpenAPI schema.
- `/mcp`: FastMCP HTTP endpoint.
- `/docs/mcp`: FastMCP docs.
- `/docs/mcp/openapi.json`: FastMCP docs OpenAPI schema.
- `/docs/mcp/tools.json`: FastMCP tool metadata.

The API also exposes an MCP server generated from the FastAPI OpenAPI schema. It gives agents the same API as MCP tools:

- `health_check`
- `subscribe_email`
- `notify_social_media`
- `create_item`
- `read_item`
- `update_item`
- `delete_item`
- `list_items`

Example agent config for MCP over HTTP:

```json
{
  "mcpServers": {
    "kyle-avrett-website-api": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Use production API origin instead of `localhost:8000` when connecting to deployed API.

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
