FROM python:3.14-slim

# directory
WORKDIR /api

# environment
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

# install runtime packages
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY uv.lock /api/
COPY api/pyproject.toml /api/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --no-dev

# copy the project
COPY api/alembic.ini /api/
COPY api/alembic /api/alembic
COPY api/src /api/src

# export virtual env
ENV PATH="/api/.venv/bin:$PATH"

# run
CMD ["fastapi", "run", "src/main.py", "--workers", "4"]
