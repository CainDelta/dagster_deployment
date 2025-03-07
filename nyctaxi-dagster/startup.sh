#!/bin/sh


# Change into the dagster src dir for execution
cd /opt/dagster/src

#set home directory
export DAGSTER_HOME=/opt/dagster/src/

# For now just execute dagster in dev mode. Later that script can just start the daemons for prod
# dagster dev -h 0.0.0.0
# Start as prod version - this also could be done in the docker container itself.
# We use this start script for convenience.
# https://docs.dagster.io/deployment/guides/docker

# For single instance we have to start the daemons first and then the webserver:
dagster-daemon run &
dagster-webserver -h 0.0.0.0

# Check https://docs.dagster.io/deployment/guides/docker for other examples
