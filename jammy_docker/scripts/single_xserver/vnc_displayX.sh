#!/bin/bash

usage() {
    echo 'usage: /start_vnc.sh <region> <internal_port> <external_port> <display>
        -- vnc ports (internal) usually start from port 5900
        -- posible regions are 1, 2, 3 or 4'
}

if [ $# -ne 4 ] ; then
    usage
    exit 1
fi

width=782
height=485
case $1 in 
    1)
        x=0
        y=0
    ;;
    2)
        x=$width
        y=0
    ;;
    3)
        x=0
        y=$height
    ;;
    4)
        x=$width
        y=$height
    ;;
    *)
        usage
        exit 1
    ;;
esac

## lanzar servidor vnc
x11vnc -display :$4 -clip $width\x$height\+$x\+$y -nopw -forever -xkb -bg -rfbport $2 &
sleep 1
## lanzar cliente noVNC
/noVNC/utils/novnc_proxy --listen $3 --vnc localhost:$2 &