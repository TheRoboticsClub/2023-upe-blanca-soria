#!/bin/bash

usage(){
    echo usage: ./start.sh display width height external_port internal_port
    echo $#
}

if [ $# -ne 5 ]
then
    usage
else
    display=$1
    width=$2
    height=$3
    external_port=$4
    internal_port=$5

    # cositas de ros
    cd 
    mkdir ws 
    cd ws 
    mkdir src
    echo 'source /opt/ros/noetic/setup.bash' >> ~/.bashrc 
    echo 'source ~/ws/devel/setup.bash' >> ~/.bashrc
    catkin build && source ~/.bashrc

    # xserver:
    /usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config ./xorg.conf $display &

    # lanzar servidor vnc
    x11vnc -display $display -nopw -forever -xkb -bg -rfbport $internal_port &

    # lanzar cliente noVNC
    /noVNC/utils/launch.sh --listen $external_port --vnc localhost:$internal_port &

    #establecer el display en el que estamos enseñando cosas
    export DISPLAY=$display

    # lanzar servidor gazebo
    gzserver &

    # configurar cliente de gazebo
    echo x=0 > ~/.gazebo/gui.ini
    echo y=0 >> ~/.gazebo/gui.ini
    echo width=$width >> ~/.gazebo/gui.ini
    echo height=$height >> ~/.gazebo/gui.ini

    # lanzar cliente de gazebo
    gzclient &

fi
