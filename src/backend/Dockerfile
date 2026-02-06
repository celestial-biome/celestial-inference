FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# 1. 依存関係の定義のみを先にコピーしてインストール（キャッシュ効率化）
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# 2. ここが重要：ソースコードをコンテナ内にコピーする
COPY . /app

# パス設定
ENV PATH="/app/.venv/bin:$PATH"

# 本番用の起動コマンド
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]