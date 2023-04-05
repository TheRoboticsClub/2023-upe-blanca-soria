#!/bin/bash

if [ $# -ne 1 ] ; then
    echo usage: ./build.sh \<name\>
    exit 1
fi
name=$1

sudo docker build --rm -t $name .