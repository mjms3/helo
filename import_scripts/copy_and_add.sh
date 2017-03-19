#!/usr/bin/sh

cp "$1" /var/lib/mysql/esp/
cat $(dirname $0)/sql_load_statement.sql | CSV_FILE="$1" envsubst | mysql -u root -p
