#!/bin/bash

if [ $# -gt 1 ] || [ $# -eq 0 ] ; then
    name=turtlebot2
else
    name=$1
fi

docker build -f Dockerfile.base -t humble_base .
docker build -f Dockerfile.turtlebot --no-cache=true -t $name .