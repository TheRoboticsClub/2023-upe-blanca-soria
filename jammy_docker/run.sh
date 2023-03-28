#!/bin/bash

if [ $# -eq 1 ] ; then
    name=$1
elif [ $# -gt 2 ] ; then
    echo 'usage: /run.sh <name of container (optional)>  <absolute local path to shared volume (optional)> '
    exit 1
else
    name=dockerRam_container
fi