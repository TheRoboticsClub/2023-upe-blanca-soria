#!/bin/bash

docker build -f Dockerfile.base -t humble_base .
docker build -f Dockerfile.ram  -t new_ram .