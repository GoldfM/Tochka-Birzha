#!/bin/sh

# Ждём готовности PostgreSQL
until pg_isready -h postgres -U postgres -d Exchange; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

echo "PostgreSQL is ready - applying migrations..."

# Применяем миграции
export PGPASSWORD="1234"
psql -h postgres -U postgres -d Exchange -f "/app/app/migrations/init.sql"

# Запускаем приложение
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080