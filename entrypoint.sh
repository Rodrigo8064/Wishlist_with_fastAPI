#!/bin/sh

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Iniciando aplicação..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "► Aplicando migrations..."
  poetry run alembic upgrade head
else
  echo "► Migrations desativadas (RUN_MIGRATIONS=false)"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Iniciando Gunicorn..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exec poetry run gunicorn fastapi_wishlist.app:app \
    --bind 0.0.0.0:8000 \
    -k uvicorn.workers.UvicornWorker \
    --workers 1 \
    --access-logfile - \
    --error-logfile - \
    --timeout 120
