#!/bin/bash

# setup environment:
root="cd /"
ros_setup="source .env && source ~/.bashrc"
copy_RAM="cp home/shared_dir/manager.py manager.py"
$root && $ros_setup && echo 'environment set'


# execute RAM from /
runram="python3.10 /manager.py 0.0.0.0 7163"
$runram
