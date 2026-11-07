#!/bin/sh
set -e

echo "[Ready2Code API] Initializing service container..."

# 1. Run Alembic database migrations
echo "[Ready2Code API] Running database migrations..."
for attempt in 1 2 3 4 5; do
  if python -m alembic -c migrations/alembic.ini upgrade head; then
    echo "[Ready2Code API] Migrations applied successfully."
    break
  else
    echo "[Ready2Code API] Database not reachable yet for migrations (attempt $attempt/5). Retrying in 2s..."
    sleep 2
  fi
done

# 2. Run idempotent database seed
python -c "
import sys, time
from scripts.seed import seed_database
for attempt in range(1, 11):
    try:
        print(f'[Ready2Code API] Attempting database initialization and seed (attempt {attempt}/10)...')
        seed_database()
        print('[Ready2Code API] Database initialized and seeded successfully.')
        break
    except Exception as e:
        print(f'[Ready2Code API] Database not ready yet: {e}. Retrying in 2s...')
        time.sleep(2)
else:
    print('[Ready2Code API] Warning: Proceeding without completing initial seed; database may already be initialized.')
" || true

exec "$@"
