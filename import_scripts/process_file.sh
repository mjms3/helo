#!/usr/bin/sh
FILE_NAME=$(basename "$1")
unzip -l "$1" | awk '{ print $4 }' | tail -n +4 | parallel --no-run-if-empty  -j4 -k $(dirname "$0")/jq_script.sh "$1" {} > "$FILE_NAME".csv
