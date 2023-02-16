#!/bin/bash

#echo $1 $2 $3
## xserver:
/usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config ./xorg.conf :$1 &
sleep 1
## lanzar servidor vnc
x11vnc -display :$1 -nopw -forever -xkb -bg -rfbport $2 &
sleep 1
## lanzar cliente noVNC
/noVNC/utils/launch.sh --listen $3 --vnc localhost:$2 &