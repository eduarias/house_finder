#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER houses;
    CREATE DATABASE houses;
    GRANT ALL PRIVILEGES ON DATABASE houses TO houses;
EOSQL