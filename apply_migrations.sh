#!/bin/sh

# Ждём готовности PostgreSQL
until pg_isready -h rc1a-i25i7m8rrl055efp.mdb.yandexcloud.net -p 6432 -U user -d tochka; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

echo "PostgreSQL is ready - applying migrations..."

# Применяем миграции
export PGPASSWORD="12341234"
psql -h rc1a-i25i7m8rrl055efp.mdb.yandexcloud.net -p 6432 -U user -d tochka -f "app/migrations/init.sql"

# Запускаем приложение
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 5001