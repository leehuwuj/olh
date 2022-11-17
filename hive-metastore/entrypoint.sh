#!/bin/sh
if [ "$1" -eq "init" ]; then
  ${HIVE_HOME}/bin/schematool -initSchema -dbType postgres
else
  ${HIVE_HOME}/bin/start-metastore
fi
    