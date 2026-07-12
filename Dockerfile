# syntax=docker/dockerfile:1.7

# ---------- Stage 1: Builder ----------
# Use a specific Python 3.14 slim image pinned to a digest-like version for reproducibility.
# `slim` variant chosen over `full` to reduce image size (no compilers/docs/tools we don't need).
FROM python:3.14-slim AS builder

# Avoid writing .pyc files and force unbuffered stdout/stderr for cleaner logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv

# Install uv (fast Python package manager) — single binary, faster and more reproducible than pip.
# Pinned version ensures the same install behavior across builds.
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /usr/local/bin/

WORKDIR /build

# Install build tools needed to compile native Python packages (e.g. numpy pulled in by vnstock).
# These live ONLY in the builder stage and are not carried to runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency manifests first for better Docker layer caching.
# This way, code changes don't bust the dependency install layer.
COPY pyproject.toml uv.lock ./

# Install production dependencies into the project venv at /opt/venv.
# --no-dev excludes dev tooling (ruff, pytest, lefthook) — production images don't need them.
# --frozen ensures the lockfile (uv.lock) is respected exactly — reproducible builds.
RUN uv sync --frozen --no-dev --no-install-project

# Now copy source code and install the project itself in editable/regular mode.
COPY src ./src
COPY README.md ./
RUN uv sync --frozen --no-dev

# ---------- Stage 2: Runtime ----------
# New clean stage with only the venv — produces a much smaller final image.
FROM python:3.14-slim AS runtime

# Run as a non-root user for security (principle of least privilege).
# UID 10001 is a high UID to avoid collisions with host users.
RUN groupadd --system --gid 10001 vnstock \
    && useradd --system --uid 10001 --gid vnstock --no-create-home --shell /usr/sbin/nologin vnstock

# Same env vars as builder for consistency.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONPATH=/app/src \
    APP_PORT=7933 \
    HOST=0.0.0.0

WORKDIR /app

# Copy only the prepared venv from the builder — not the build tooling, source caches, or uv itself.
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/src ./src

# Ensure the non-root user owns the application files.
RUN chown -R vnstock:vnstock /app

USER vnstock

EXPOSE 7933

# Production server: granian (Rust-based ASGI server) — high performance, low memory.
# `--interface asgi` matches the built app, `--workers 1` (scale via replicas, not in-proc workers
# for a stateful LLM agent), `--log-level info` for production, `--host 0.0.0.0` to accept external traffic.
CMD ["granian", "src.api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "7933", \
     "--interface", "asgi", \
     "--workers", "1", \
     "--log-level", "info"]
