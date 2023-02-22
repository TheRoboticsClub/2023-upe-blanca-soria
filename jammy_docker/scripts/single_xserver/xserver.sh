#!/bin/sh

if [ $# -ne 1 ] ;then
    echo 'usage: number of argumentws is invalid 
                ./xerver.sh <display>'
    exit 1
fi
## xserver:
cd /
/usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config ./xorg.conf :$1 &
sleep 1