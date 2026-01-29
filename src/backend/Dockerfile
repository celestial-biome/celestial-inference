# 1. uv 公式イメージを使用してビルド環境を構築
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# 依存関係のインストール (キャッシュを利用)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev

# 2. 実行用の軽量イメージを作成
FROM python:3.12-slim-bookworm

WORKDIR /app

# ビルダーから仮想環境をコピー
COPY --from=builder /app/.venv /app/.venv

# アプリケーションコードをコピー
COPY . .

# パス設定
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Cloud Run の PORT 環境変数に対応するため、シェル形式ではなく実行形式で記述
# fastapi run を使用し、0.0.0.0 で Listen する
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8080"]