# Base image
FROM python:3.12-slim AS base

# Environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=2

# Update and clean the base image
RUN apt update && \
    apt upgrade -y && \
    apt clean && \
    rm -rf /var/cache/apt/*

# Base image for uv tool
FROM base AS uv
ENV UV_PYTHON_PREFERENCE=only-system \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local/

# Add uv tool
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV PATH="/root/.local/bin:${PATH}"

# Development image setup
FROM uv AS dev
WORKDIR /app

# Copy dependency files
COPY grpc_api/pyproject.toml grpc_api/uv.lock ./

# Install dependencies in development mode
RUN uv sync --frozen

# Production image setup
FROM uv AS prod
WORKDIR /app

# Optimize Python bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project and dependency files
COPY grpc_api/pyproject.toml grpc_api/uv.lock ./
RUN uv sync --no-dev

# Copy application source code
COPY grpc_api/src/grpc_api/ /app/grpc_api

# Set a non-root user for security
RUN adduser --disabled-password --gecos '' myuser && \
    chown -R myuser:myuser /app

# Switch to non-root user
USER myuser

# Run the gRPC server
CMD ["python", "-m", "grpc_api.main"]
