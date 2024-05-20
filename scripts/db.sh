#!/bin/sh

host="db"
port="5432"

echo "Ожидание доступности $host:$port..."

# Попытка подключения к указанному хосту и порту
while ! pg_isready -h "$host" -p "$port" >/dev/null 2>&1; do
  sleep 2
done

echo "Connected $host:$port..."