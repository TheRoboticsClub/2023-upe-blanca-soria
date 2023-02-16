#!/bin/bash

usage(){
    echo 'usage: ./start_all.sh width height
    width and height are used for every window possible'
    exit 1
}

# $1 = display, $2 = internal port , $3 = external port
start_vnc_service(){
    # xserver:
    /usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config ./xorg.conf :$1 &
    sleep 1
    ## lanzar servidor vnc
    x11vnc -display :$1 -nopw -forever -xkb -bg -rfbport $2 &
    sleep 1
    ## lanzar cliente noVNC
    /noVNC/utils/launch.sh --listen $3 --vnc localhost:$2 &
}

if [ $# -ne 2 ]
then
    usage
fi

width=$1
height=$2

# lanzar gazebo:
start_vnc_service 0 5900 6080
gzserver &
# configurar cliente de gazebo
echo [geometry] > ~/.gazebo/gui.ini && \
echo x=0 >> ~/.gazebo/gui.ini && \
echo y=0 >> ~/.gazebo/gui.ini && \
echo width=$width >> ~/.gazebo/gui.ini && \
echo height=$height >> ~/.gazebo/gui.ini
DISPLAY=:0 gzclient &

sleep 2
 
# lanzar consola:
start_vnc_service 1 5901 1108 
DISPLAY=:1 xterm -geometry $width\x$height -fa 'Monospace' -fs 10 -bg black -fg white &

sleep 2
 
# lanzar Rviz:
start_vnc_service 2 5902 2303
roscore &
cp /home/shared_dir/default.rviz /opt/ros/noetic/share/rviz/default.rviz
DISPLAY=:2 rviz &

# lanzar gui:
start_vnc_service 3 5903 1905
DISPLAY=:3 python3 home/shared_dir/showAlfil.py &# $width $height

