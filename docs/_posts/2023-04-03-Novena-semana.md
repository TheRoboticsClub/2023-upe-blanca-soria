---
title: "Reorganizacion CustomRobots: Novena Semana"
date: 2023-02-16
categories:
  - CustomRobots
tags:
---

Esta semana la tarea ha estado enfocada en reorganizar la rama `humble-devel` de CustomRobots como un repositorio autonoctenido que contenga todo lo necesario para ejecutar un aplicaion robótica. De esta forma tendra una fomra pareceida a la de RoboticsAcademy pero toda la parte web se queda en este repositorio mientras que en CustomRobots/humble-devel tendremos el manager, los modelos de robots y mundos y todo el tema de dockerización. En esta primera aproximación tambien tendermos un directorio `/tmp` con la parte web de react, para así tener un entrno autocontenido.

Primero ha habido que mover el directorio scripts que tenia en mi repositorio de practicas, donde se encontraba el nuevo RAM en ROS2 y todos los scripts de docker. Los cambios mas importantes han estado en los Dockerfiles y el fichero .env ya que al estar todo reorganizado de otro modo las rutas a los distintos recursos son distintas. Una vez cambiadas las varibales de entorno y rutas he podido actualizar varias lineas del manager para que no haya que hacer ninguna trampa dentro del mismo; esto ha sido posible por el hecho de tener una web en este directorio y haber podido crear ejercicios especificos para ROS2 con una configuración especializada con:
- El nombre de los ejercicios conteniendo solo los de ROS2
- El nombre de los launcher para ROS2

Además de esta reorganización básica he convertido el ahora directorio CustomRobots en un paquete ROS, de esta manera cuando necesitemos algun recurso dentro de un paquete solo tendremos que añadir ciertas lineas a un CMakeLists.txt que tenemos en CustomRobots. Las intrucciones para añadir robots etc. están en [este README](https://github.com/JdeRobot/CustomRobots/blob/humble-devel/CustomRobots/README.md). Los mas importante de esto es que en todos los .world , .urdf, .xacro etc. en vez de tener que buscar cual es el paquete que contiene ciertos modelos, todos estarán contenidos en custom_robots, y por tanto tambien en estos ficheros deberemos especificarlo.

El repositorio entonces donde estaré trabajando de ahora en adelante es [humble-devel](https://github.com/JdeRobot/CustomRobots/tree/humble-devel)

