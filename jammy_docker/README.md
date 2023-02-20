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
El nombre del container es opcional al igual que el volumen. Si no introducimos ningun nombre *container name* será `turtlebot2_container`. Si introducimos una ruta **absoluta** como segunda opcion *shared volume* se creará una carpeta compartida entre el host y el contenedor.

## Para entrar en el contenedor con una terminal (bash):
~~~
docker exec -it <container name> /bin/bash
~~~

## Dentro del contenedor
Una vez ejecutamos *run.sh* se nos abrirá una terminal dentro del contenedor. Nuestro directorio de trabajo actual es el workspace de ros2 humble con los respectivos directorios rcs, install build y logs. 

Para poder ver las salidas gráficas de nuestro docker tenemos en el directorio `/` varios scripts; 
- Para iniciar un xserver, servidor vnc y cliente noVNC podemos usar `/start.sh` indicando los puertos y displays especificos ó `/start_4windows.sh` que inicia los 4 displays que estan ya configurados en la página windows.html de https://github.com/TheRoboticsClub/2023-upe-blanca-soria/tree/main/frontend :
~~~
/start_vnc.sh <display> <internal_port> <external_port>
~~~ 

- El script `/start_console.sh` inicia una consola en el display :2 y puerto 1108 

- El script `/kill_all.sh` mata todos los procesos de gazebo, rviz servidores x y servicios vnc.


Dentro del workspace tenemos un script `/home/turtlebot2_ws/empty_world_turtlebot.sh` que inicia un servidor y cliente de gazebo, rviz2 y spawnea el turtlebot2 dentro de este mundo vacio. 

Además, si tenemos el turtlebot2 iniciado en cualquier mundo podremos visualizar su cámara en la ventana GUI ejecutando:
~~~
DISPLAY=:3 ros2 run gui_pkg showgui
~~~

### Ejemplo de ejecución

desde el directorio jammy_docker en el host ejecutamos:
~~~
./build.sh
./run.sh turtlebot2_container /ruta/a/directorio/de/trabajo
~~~
Una vez dentro del contenedor ejecutaremos los siguientes comandos:
~~~
/start_4windows.sh
/start_console.sh
DISPLAY=:3 ros2 run gui_pkg showgui &
./empty_world_turtlebot.sh
~~~
Todo esto generará en windows.html:



