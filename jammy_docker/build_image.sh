#!/bin/bash

docker build -f Dockerfile.base -t my_humble_base .
docker build -f Dockerfile.ram  -t new_ram .