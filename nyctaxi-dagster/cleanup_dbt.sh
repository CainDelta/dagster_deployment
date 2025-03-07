#!/bin/bash
docker exec -t "dagster" sh -c "cd /opt/dagster/src/nyctaxi_dagster/nyctaxi_dbt/ && dbt clean --profiles-dir config"

df -H
