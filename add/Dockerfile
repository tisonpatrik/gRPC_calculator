FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=2

RUN apt update && \
    apt upgrade -y && \
    apt clean && \
    rm -rf /var/cache/apt/*

# Stage: UV setup
FROM base AS uv
ENV UV_PYTHON_PREFERENCE=only-system
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_CACHE=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV PATH="/root/.local/bin:${PATH}"

# Stage: Development setup
FROM uv AS dev
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen # --no-install-project

# Stage: Production setup
FROM uv AS prod
ENV UV_COMPILE_BYTECODE=1
EXPOSE 50051
WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --locked

COPY add/ ./add

# Set PYTHONPATH, aby Python našel správnou cestu
ENV PYTHONPATH=/app

# Set a non-root user for security
RUN adduser --disabled-password --gecos '' myuser

# Ensure /app directory exists and set ownership to myuser
RUN chown -R myuser:myuser /app

USER myuser

# CMD pro spuštění pouze gRPC serveru
CMD ["python", "add/src/main.py"]
