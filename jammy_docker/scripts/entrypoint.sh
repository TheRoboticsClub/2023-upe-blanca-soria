#!/bin/bash

# setup environment:
root="cd /"
ros_setup="source .env && source ~/.bashrc"
$root && $ros_setup && echo 'environment set'

# execute RAM from /
runram="python3 /manager.py 0.0.0.0 7163"
$runram
