#!/bin/bash

if [$# -eq 1 && -n $1]
then
    name=$1
elif [$# -gt 1]
    echo 'usage: /run.sh <name of container (optional)>'
    exit 1
else
    name=turtlebot2_container
fi

sudo docker run --gpus all --name $name --rm -it -p 2303:2303 -p 1905:1905 -p 8765:8765 -p 6080:6080 -p 6081:6081 -p 1108:1108 -p 6082:6082 turtlebot2