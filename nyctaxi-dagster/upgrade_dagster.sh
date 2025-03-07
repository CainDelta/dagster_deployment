#!/bin/sh

#script will build docker image to pull latest versions of dagster
docker login -u **** -p **** docker.io
docker pull deltambx/dagster_docker:latest
docker stop dagster
docker rm dagster
docker run -d -v $(pwd):/opt/dagster/src --restart=on-failure -p 3000:3000 --name dagster  --log-driver json-file --log-opt max-size=1024m    --log-opt max-file=3 deltambx/dagster_docker:latest
