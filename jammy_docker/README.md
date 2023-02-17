# DOCKER CON TURTLEBOT2

Esta carpeta contiene los DockerFiles necesarios para generar una imagen docker con Ubuntu 22.04, ROS2 Humble, Rviz2, Gazebo 11 y todas las dependencias necesarias para simular el robot Turtlebot2.

## Generar un contenedor
La imagen `turtlebot2` se genera a partir del Dockerfile basico (con ubuntu, ROS2, Rviz y Gazebo) y el Dockerfile del Turtlebot2. Para conseguirlo ejecutar: 
~~~
./build_image.sh
~~~

Para crear un contenedor ejecutaremos:
~~~
./run.sh <container name> <shared volume>
~~~
El nombre del container es opcional. Si no introducimos ningun nombre *container name* será `turtlebot2_container`.

## Para entrar en el contenedor con una terminal (bash):
~~~
docker exec -it <container name> /bin/bash
~~~
