---
title: "Cuarta Semana"
date: 2023-02-16
categories:
  - blog
tags:
  - Introduccion
  - Docker
---

Esta semana me he dedicado a replicar el docker con ubuntu-jammy: 22.04 que tienen mis compañeros que estan haciendo el TFG. La motivación es hacer un nuevo RAM que tenga ROS2 Humble en vez de ROS noetic.

Para ello inicialmente he estado trabajando en una imagen docker base en la que tenemos Gazebo, ROS" Humble, Rviz2, la base de ubuntu 22 y los programas de servidor X, VNC y websockets. A parte, en un segundo docker están las partes más específicas de la aplición que se va a correr: el sistema de ficheros con los ejecutables necesarios, la compilacion del workspace de ROS y los puertos abiertos que tendrá el contenedor hacia el host. Además esta imagen contiene una sucesión de scripts parecida a los scripts para ubuntu-noetic pero con un mejor funcionamiento. Estos scripts permiten inciar los 4 visores `start_4windows.sh`, inicial una consola en su visor correspondiente `star_console.sh`, iniciar únicamente 1 visor `start_vnc.sh`, matar todos los procesos de la máquina `kill_all.sh` y abrir un mundo de gazebo vacío con el turtlebot en un visor y Rviz en otro visor `empty_world_turtlebot.sh` (este último ya estaba en la imagen de los compañeros).

La intención ha sido poder ejecutar un programa en ROS2 en frío dentro del docker, pudiendo visualizarlo en la página windows.html. Para ello he copiado de mis compañeros los directorios que contienen los mundos de gazebo, modelos y ejecutables del robot Turtlebot2. Con ellos ha sido sencillo ejecutar un mundo vacío con el turtlebot, además del rviz con el mismo y una consola. He añadido un paquete ROS2 en python para poder ejecutar un nodo sencillo que muestre un GUI en el 4º visor. Este nodo simplemente se subscribe a la cámara del turtlebot y muestra en este 4º visor lo que el robot está viendo:

<p align="center">
<iframe width="560" height="315" src="https://youtu.be/tIk096Ulmyg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</p>


En el video se puede apreciar que hay que mejorar el tamaño del servidor/cliente VNC para que las ventanas se ajusten a los visores, pero es una idea general y se ve que puede funcionar.

Además de la ejecución he estado dedicandole tiempo a estudiar el funcionamiento del nuevo RAM, que implementa una máquina de estados y separa su funcionamiento en varias clases.