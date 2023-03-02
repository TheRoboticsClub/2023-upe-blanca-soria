#!/bin/sh

# setup environment:
root="cd /"
ros_setup="source .env"
$root $ros_setup

# execute RAM from /
runram="python3 /manager.py 0.0.0.0 7163"
$runram
