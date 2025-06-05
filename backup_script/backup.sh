#!/bin/bash

#replace path with the actual path
export PGPASSFILE="/path/.pgpass"


timestamp=$(date +"%Y-%m-%d_%H-%M-%S")


backup_path="/path/${timestamp}.backup"

# /usr/pgsql-17/bin/pg_dump is the path to my pg_dump binary, replace with your actual path
/usr/pgsql-17/bin/pg_dump \
  -U user \
  -h localhost \
  -d database \
  -F c -b -v \
  -f "$backup_path"

gpg --batch --yes --passphrase "S@fePassw0rd" --symmetric --cipher-algo AES256 "$backup_path"
rm "$backup_path"
