---
title: "Nuevo RAM en ROS2 con página simple: Sexta semana"
date: 2023-02-16
categories:
  - RAM
  - Exercise
tags:
---

El trabajo de esta semana consiste en modificar las plantillas de los ejercicios para poder ejecutar una aplicación en ROS2 de la misma forma que se hace en Unibotics, pero con mi página sencilla.

## Cómo funciona la aplicación en el nuevo RAM

Para ejecutar la aplicación introducida por el usuario se hace una mezcla entre su código y una plantilla que se está corriendo continuamente, pudiendo así cambiarse el código fuente en caliente. Para ello desde el manager se crea un objeto que llamamos **application**. Se crea un objeto *Exercise*[1] que hereda de *CompatibilityExerciseWrapper*[2] y a su vez este de *IRoboticsPythonApplication*[3]; en este objeto tenemos el init de la clase que se encargará de llamar al init de *CompatibilityExerciseWrapper*. En conclusión, la clase que implemtena la aplicaión es *CompatibilityExerciseWrapper*; esta se encarga de lanzar 2 subporcesos, uno para el **exercise.py** y otro para el **gui.py**, y se convierte en cliente de ambos, que son Websocket Servers. A partir de ahí este es el que recibe comandos desde el manager, que a su vez fueron mandados desde el browser se encarga de intercambiarlos con el exercise y el gui; además es el encargado de pausar/despausar/reiniciar las físicas de Gazebo cuando el manager le manda un Stop, Resume etc. Finalmente si el mensaje recibido del manager es código a guardar/ejecutar se pasará previamente por un Linter antes de mandárselo a exercise.py.

A partir de ahí la ejecución se enfoca en los ficheros *exercise.py* y *gui.py*, que usan otras clases que se encuantran en el mismo directorio del ejercicio. Exercise.py recibe comandos como CODE, FREQ, PING, STOP, RESET entre otras; dependiendo de cada comando ejecutará una serie de funciones. Los comandos de FREQ y PING son pedidos por el browser periódicamente para saber el estado del ejercicio y devuelven a la aplicación los datos necesarios. El comando CODE puede llevar el subcomando SAVE, LOAD o nada , que guardarán o sacarán el código del usuario en un fichero. Si no hay ningún subcomando el código se dividirá en sus partes secuencial e iterativa y se lanzará un proceso **brain.py** que es le que se encarga de ejecutar el código. Los comandos STOP, RESET y PLAY actuan sobre eventos de este proceso para parar, reinciar etc. el mismo. Dependiendo del ejercicio habrá otros comandos específicos como un teleoperador etc.

Gui.py comaparte valores *SharedValues* con el Hal y con User_code para enviar al browser una imagen, velocidad u otro tipo de datos interesantes.

##### Direcciones a los ficheros:
- [] Todos los ficheros del ejercicio como hal.py, exercise.py, gui.py, brain.py etc. se encuentran en el directorio: `$EXERCISE_FOLDER` , que estará en `RoboticsAcademy/exercises/static/exercises/<ejercicio>`.
- [1] Exercise: `$EXERCISE_FOLDER/entrypoint/exercise.py`
- [2] CompatibilityExerciseWrapper: `src/libs/application/compatibility/exercise_wrapper`
- [3] IRoboticsPythonApplication: `src/manager/application/robotics_python_application_interface.py`


### Cambios

Para adaptar el funcionamiento de este nuevo RAM a ROS2 he tenido que cambiar:
- En exercise_wrapper.py la manera en la que se lanzan los servicios de gazebo.
- En `$EXERCISE_FOLDER/interfaces` las interfaces de ROS a ROS2, cambiando los publicadores, subscriptores e interfaces de rospy a **rclpy**.
- En hal.py he tenido que añadir un rclpy.spin_once() para que el subscriptor de la imagen pueda recibir imagenes del robot.
- Pequeños cambios en los includes de otros ficheros para que no aparezca *rospy*.

## RESULTADO

Finalmente he conseguido que se ejecute un código sencillo lanzado ya por el manager en mi página sencilla. Por lo que el resultado está ya funcionando destre de la rama *simple_connection* de mi repositorio. Es resultado en este [video](https://youtu.be/KHQ2GiObIwc).