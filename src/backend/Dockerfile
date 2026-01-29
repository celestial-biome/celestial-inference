FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# 依存関係のインストール (本番用なので --no-dev を推奨)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# 本番用の起動コマンド
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]