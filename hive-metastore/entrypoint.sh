#!/bin/bash

echo "Command: $1"

if [ "$1" = "init" ]; then
  echo "Start init schema"
  ${HIVE_HOME}/bin/schematool -initSchema -dbType postgres
elif [ "$1" = "run" ]; then
  echo "Starting metastore server"
  ${HIVE_HOME}/bin/start-metastore
else
  echo "Missing command: run or init"
fi
