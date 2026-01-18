#!/bin/bash
set -e

echo "========================================"
echo "Backend Startup Script"
echo "========================================"

# Wait for PostgreSQL to be ready
echo ""
echo "[1/4] Waiting for PostgreSQL to be ready..."
MAX_TRIES=30
COUNT=0

until pg_isready -h postgres -U mastermind > /dev/null 2>&1 || [ $COUNT -eq $MAX_TRIES ]; do
  COUNT=$((COUNT+1))
  echo "  Attempt $COUNT/$MAX_TRIES: PostgreSQL is unavailable - sleeping"
  sleep 2
done

if [ $COUNT -eq $MAX_TRIES ]; then
  echo "  ✗ PostgreSQL did not become ready in time"
  exit 1
fi

echo "  ✓ PostgreSQL is ready"

# Run database migrations
echo ""
echo "[2/4] Running database migrations..."
if alembic upgrade head; then
  echo "  ✓ Migrations completed successfully"
else
  echo "  ✗ Migrations failed"
  exit 1
fi

# Seed AI users (idempotent)
echo ""
echo "[3/4] Seeding AI users..."
if python scripts/seed_ai_users.py; then
  echo "  ✓ AI users seeding completed"
else
  echo "  ✗ AI users seeding failed"
  exit 1
fi

# Start the application
echo ""
echo "[4/4] Starting Uvicorn server..."
echo "========================================"
echo ""

exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
