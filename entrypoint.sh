#!/bin/sh

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Iniciando aplicação..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "► Aplicando migrations..."
poetry run alembic upgrade head

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Iniciando Gunicorn..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exec poetry run gunicorn fastapi_wishlist.app:app \
    --bind 0.0.0.0:8001 \
    -k uvicorn.workers.UvicornWorker \
    --workers 1 \
    --access-logfile - \
    --error-logfile - \
    --timeout 120
