---
title: "Nuevo RAM en ROS2 con página simple: Quinta semana"
date: 2023-02-16
categories:
  - HTML
  - JavaScript
  - RAM
  - launch
tags:
---

Esta semana he comenzado a introducir el nuevo RAM de RoboticsAcademy en mi docker con ROS2, todo ello en la rama simple_connection. He conseguido elaborar una comunicación entre la máquina docker y el browser con una interfaz sencilla basada en mi estructura anterior de 4 ventanas. En este caso se trata de la misma estructura pero esta vez he añadido varios botones que aparecen o desaparecen en funciona al estado en el que se encuatra el manager (que es una máquina de estados). Además , para no incluir un editor de texto hay un input de código que abre un buscador del sistema para subir un fichero, que será el código a ejecutar. Por ùltimo también hay un boton de vistas que permite recargar las vistas sin tener que recargar toda la página, pudiendo así visualizar las mismas en cualquier estado.

Otro frente ha sido la comunicación con el manager, en JavaScript. He utilizado la API que se usa enla implementeción completa del frontend para poder comunicar mi html sencillo con el manager de la misma manera que lo hace la parte REACT de la implementación final. Esta API permite enviar y recbir mensajes con el manager y de momento he conseguido que, sustituyendo casi todas la lineas que hacen alguna fucnion real, el manager pueda moverse y transicionar por todos los estados, pudiendo subir un fichero de código y ejecutando un Linter que se encarga de la comprobacion sintactica del mismo. 

A finales de semana he conseguido **launchear** el turtlebot junto con rviz2 , aunque este sin la configuración adecuada, y la consola en las vistas del html. La imagen docker está configuradad para ejecutar directamente `entrypoint.sh` pero para probar cosas en el video de demostración se ve como se lanza el manager manuelamente: [launching with manager](https://youtu.be/78ilM0IJZAI)