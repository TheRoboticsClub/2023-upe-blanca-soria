#!/bin/sh

if [ $# -ne 3 ] ;then
    echo 'usage: number of arguments is invalid 
                ./start_console.sh <x> <y> <display>'
    exit 1
fi

DISPLAY=:$3 xterm -geometry 94x28+$1\+$2 -fa 'Monospace' -fs 10 -bg black -fg white &