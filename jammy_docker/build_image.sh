#!/bin/bash

docker build -f Dockerfile.base -t humble_base .
docker build -f Dockerfile.ram --no-cache=true -t new_ram .