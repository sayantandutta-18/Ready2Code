#!/bin/sh
set -e

echo "[Ready2Code API] Initializing service container..."

# Run migrations and idempotent seed on startup
python -c "
import sys, time
from scripts.seed import seed_database
for attempt in range(1, 11):
    try:
        print(f'[Ready2Code API] Attempting database initialization (attempt {attempt}/10)...')
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
