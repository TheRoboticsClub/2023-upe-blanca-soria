#!/bin/bash

# setup environment:
root="cd /"
ros_setup="source .env"
copy_RAM="cp home/shared_dir/manager.py manager.py"
$root && $ros_setup && $copy_RAM && echo 'environment set'


# execute RAM from /
runram="python3.10 /manager.py 0.0.0.0 7163"
$runram
