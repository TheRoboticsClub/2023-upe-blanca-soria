#!/bin/bash
docker build -f Dockerfile.base -t basic-jammy .
docker build -f Dockerfile --no-cache=true -t ubuntu-22 .