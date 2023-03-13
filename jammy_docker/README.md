# DOCKER CON NUEVO RAM

Esta carpeta contiene los DockerFiles necesarios para generar una imagen docker con Ubuntu 22.04, ROS2 Humble, Rviz2, Gazebo 11 y lo necesario para ejecutar un contenedor que sea capaz de hacer una comunicacion sencilla entre la máquina y un servidor http como el que podemos ejecutar dentro de `/simple_connection`.

## Generar un contenedor
La imagen `new_ram` se genera a partir del Dockerfile basico (con ubuntu, ROS2, Rviz y Gazebo) y el Dockerfile del nuevo RAM. Para conseguirlo ejecutar: 
~~~
./build_image.sh
~~~

Para crear un contenedor ejecutaremos:
~~~
./run.sh <container name> <shared volume>
~~~
El nombre del container es opcional al igual que el volumen. Si no introducimos ningun nombre *container name* será `dockerRam_container`. Si introducimos una ruta **absoluta** como segunda opcion *shared volume* se creará una carpeta compartida entre el host y el contenedor.

## Para entrar en el contenedor con una terminal (bash):
~~~
docker exec -it <container name> /bin/bash
~~~

## Dentro del contenedor
 Al ejecutar `run.sh` se nos abrirá una terminal dentro del contenedor. Para comenzar a ejecutar el RAM tendremos que lanzar `entrypoint.sh`, que se encuentra en `/`. Una vez ejecutado podemos ver los logs del manager, ya que se han sustituido todos ellos por prints para poder ver con facilidad y en todo momento en que punto se encuentra la máquina de estados.

## Ejecutar Webserver
Para poder comunicarnos con el manager deberemos ejecutar dentro de la carpeta `simple_connection` un servidor http:
~~~
python -m http.server
~~~
Y dentro de `localhost:8000/windows.html` podremos ver la página sencilla del siguiente modo:


![Captura de pantalla de 2023-03-03 14-36-10](https://user-images.githubusercontent.com/79047431/222733830-625b6df0-c959-43cb-ac86-992305bc13f8.png)

Para conectar ambas partes debemos recargar esta página una vez hemos iniciado `entrypoint.sh`, y por tanto el manager. Cuando lo hacemos el manager pasa directamente al estado: CONNECTED. A partir de ahi podemos hacer DISCONNECT o LAUNCH. Para saber cuales son las posibilidades del siguiente estado los botones desapareceran y aparecerán tras transicionar, pero en el primer instante aparecerán todas los botones. Se recomienda hacer un DISCONNECT incialmente para seguir el flujo de la máquina de estados con mas facilidad.


![States_machineRAM](https://user-images.githubusercontent.com/79047431/224103776-18e710d1-acc3-4604-8e97-6122009fc544.png)

