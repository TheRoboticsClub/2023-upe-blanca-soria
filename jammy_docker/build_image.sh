#!/bin/bash
docker build -f Dockerfile.base -t humble_base .
docker build -f Dockerfile.turtlebot --no-cache=true -t  turtlebot2 .