---
title: "Nuevo RAM en ROS2 con página oficial: Septima semana"
date: 2023-02-16
categories:
  - RAM
  - launch
  - exercise
tags:
---

Esta semana ha consistido en hacer que la aplicaión completa que ya funcionaba en una pagina encilla funcione en la página oficial con REACT.

Para ello inicialmente he conseguido que el escenario y robot se lancen (launch) correctamente mediante el fichero de configuración que le manda el servidor Django. En este fichero se establecen varias capas, la primera es una ROS_API que se encarga de lanzar el escenario y el robot en gazebo; posterioirmente hay varias capas que lanzan servidores y clientes VNC para los visualizadores de la consola , gazebo etc. Los ficheros que se encargan de lanzar esto han cambiado debido a que en ROS2 el sistema de launch es distinto y basta con ejecutar un comando `ros2 launch <fichero>.launch.py`. Para poder entonces launchear un ejercicio he creado un fichero.launch.py que puede servir de plantilla para el resto de launchers de otros ejercicios; este se encuentra en `$EXERCISE_FOLDER/launch`.

Una configuración de ejemplo recibida en el manager seria:

~~~
{
  "application": {
    "type": "python",
    "entry_point": "$EXERCISE_FOLDER/web-template/entry_point/exercise.py",
    "class_name": "Exercise",
    "params": ""
  },
  "launch": {
    "0": {
      "type": "module",
      "module": "ros_api",
      "resource_folders": [
        "$EXERCISE_FOLDER/web-template/launch"
      ],
      "model_folders": [
        "$CUSTOM_ROBOTS_FOLDER/f1/models"
      ],
      "plugin_folders": [
      ],
      "parameters": [],
      "launch_file": "$EXERCISE_FOLDER/web-template/launch/simple_line_follower_ros_headless_${circuit}.launch"
    },
    "1": {
      "type": "module",
      "module": "vnc",
      "resource_folders": [
        "$EXERCISE_FOLDER/web-template/launch"
      ],
      "model_folders": [
        "$CUSTOM_ROBOTS_FOLDER/f1/models"
      ],
      "plugin_folders": [
      ],
      "parameters": [],
      "launch_file": "$EXERCISE_FOLDER/web-template/launch/simple_line_follower_ros_headless_${circuit}.launch"
    }
  }
  "exercise_id": "simple_follow_line"
}
~~~

En el exercise.py he tenido que cambiar algun detalle para que todo funcione bien con la página oficial y se pueda visualizar correctamente el gui en la página.

Para que todo esto funcione he hecho alguna trampilla para que se ejecute de manera correcta. No existe de momento un ejercicio en la página que este configurado para mandar la configuración específica en ROS2 por lo que dentro de manager.py y launcher_ros_api.py he tenido que añadir alguna modificación que cuando se mande correctamente la configuración habrá que quitar. El ejercicio nuevo se crea durante la creación de la imagen docker en `/RoboticsAcademy/exercises/static/esxercises/follow_line_newmanager_ros2` por lo que:
- en manager.py cuando se establece la variable de entorno *$EXERCISE_FOLDER* se establece la ruta encima menscionada.
- en el fichero .env he tenido que cambiar la ruta hacia los modelos de los robots, ya que en la rama **humble-devel** del repositorio CustomRobots la organizacion de los ficheros es distinta.
- en launcher_ros_api.py he tenido que añadir al launcher_file de la configuracion un `.py` para qeu se dirija correctamente al fichero en cuestión.

Con todo esto y algun otro detalle he conseguido el siguiente [resultado](https://youtu.be/KHQ2GiObIwc).

