set -e

dbname=lottery

psql -c "CREATE DATABASE \"${dbname}\";"