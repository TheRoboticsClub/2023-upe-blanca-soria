#!/bin/bash

. install/setup.bash

cp /home/.display_conf/default.rviz /opt/ros/humble/share/rviz_common/default.rviz
DISPLAY=:1 rviz2 &

export DISPLAY=:0
# cat /home/.display_conf/gz_default.txt > /ruta/a/gui.ini??
ros2 launch turtlebot2 spawn_model.launch.py &
ros2 launch gazebo_ros gazebo.launch.py