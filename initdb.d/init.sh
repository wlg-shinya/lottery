set -e

dbname=lottery

psql -c "CREATE DATABASE \"${dbname}\";"

# CREATE TABLE lotteries (id serial, user_id integer NOT NULL, text text NOT NULL, title text NOT NULL);
# CREATE TABLE users (id serial);
psql -d ${dbname} -f /docker-entrypoint-initdb.d/ddl # pg_dump -d lottery -U postgres --schema-only > ddl
psql -d ${dbname} -f /docker-entrypoint-initdb.d/dml # pg_dump -d lottery -U postgres --data-only > dml
