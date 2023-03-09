#!/bin/bash

if [ $# -eq 1 ] ; then
    name=$1
elif [ $# -gt 2 ] ; then
    echo 'usage: /run.sh <name of container (optional)>  <absolute local path to shared volume (optional)> '
    exit 1
else
    name=dockerRam_container
fi

if [ $# -eq 2 ] && [ -n $2 ] ; then
    docker run --name $name -v $2:/home/shared_dir --rm -it -p 2303:2303 -p 1905:1905 -p 8765:8765 -p 6080:6080 -p 6081:6081 -p 1108:1108 -p 6082:6082 -p 7163:7163 new_ram bash
else
    docker run --name $name --rm -it -p 2303:2303 -p 1905:1905 -p 8765:8765 -p 6080:6080 -p 6081:6081 -p 1108:1108 -p 6082:6082 -p 7163:7163 new_ram bash
fi