#!/bin/sh

/single_xserver/xserver.sh 0
sleep 1
/single_xserver/vnc_displayX.sh 1 5900 6080 0
/single_xserver/vnc_displayX.sh 2 5901 6081 0
/single_xserver/vnc_displayX.sh 3 5902 1108 0
/single_xserver/vnc_displayX.sh 4 5903 6082 0