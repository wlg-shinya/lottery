set -e

dbname=lottery

psql -c "CREATE DATABASE \"${dbname}\";"
psql -d ${dbname} -c "CREATE TABLE lotteries();"
psql -d ${dbname} -c "CREATE TABLE users();"
psql -d ${dbname} -c "CREATE TABLE tokens();"
