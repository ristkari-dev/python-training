# syntax=docker/dockerfile:1.7

# --- Stage 1: build the static dist/ ---
FROM python:3.13-slim AS builder
WORKDIR /src

# uv: copy the static binary from the official image (no curl/install step).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the whole repo; build_index needs lessons/, shared/, and the tool.
COPY . .

# Install the workspace (members include build_index) without dev tools,
# then render the landing page + copy decks + vendored reveal.js into /dist.
RUN uv sync --frozen --all-packages --no-dev \
    && uv run --no-dev --all-packages python -m build_index \
        --lessons /src/lessons \
        --shared /src/shared/reveal \
        --out /dist

# --- Stage 2: serve dist/ with non-root nginx ---
FROM nginxinc/nginx-unprivileged:alpine
USER root
COPY deploy/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=builder /dist /usr/share/nginx/html
# Drop back to the unprivileged user the image ships with (UID 101).
USER 101
EXPOSE 8080
