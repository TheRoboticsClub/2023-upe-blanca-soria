//import * as log from "loglevel";
//import { v4 as uuidv4 } from "uuid";

var fileContent_loaded = false;
var fileContent;
var actual_id = 0;

const CommsManager = (address) => {
    let websocket = null;
  
    //log.enableAll();
  
    const events = {
      RESPONSES: ["ack", "error"],
      UPDATE: "update",
      STATE_CHANGED: "state-changed",
    };
  
    //region Observer pattern methods
    const observers = {};
  
    const subscribe = (events, callback) => {
      if (typeof events === "string") {
        events = [events];
      }
      for (let i = 0, length = events.length; i < length; i++) {
        observers[events[i]] = observers[events[i]] || [];
        observers[events[i]].push(callback);
      }
    };
  
    const unsubscribe = (events, callback) => {
      if (typeof events === "string") {
        events = [events];
      }
      for (let i = 0, length = events.length; i < length; i++) {
        observers[events[i]] = observers[events[i]] || [];
        observers[events[i]].splice(observers[events[i]].indexOf(callback));
      }
    };
  
    const unsuscribeAll = () => {
      for (const event in observers) {
        observers[event].length = 0;
      }
    };
  
    const subscribeOnce = (event, callback) => {
      subscribe(event, (response) => {
        callback(response);
        unsubscribe(event, callback);
      });
    };
  
    const dispatch = (message) => {
      const subscriptions = observers[message.command] || [];
      let length = subscriptions.length;
      while (length--) {
        subscriptions[length](message);
      }
    };
    //endregion
  
    // Send and receive method
    const connect = () => {
      return new Promise((resolve, reject) => {
        websocket = new WebSocket(address);
  
        websocket.onopen = () => {
          //log.debug(`Connection with ${address} opened`);
          console.log(`Connection with ${address} opened`);
          send("connect")
            .then(() => {
              console.log("RESOLVE CONNNNECT")
              resolve();
            })
            .catch(() => {
              console.log("REJECT CONNNNECT")
              reject();
            });
        };
  
        websocket.onclose = (e) => {
          // TODO: Rethink what to do when connection is interrupted,
          //  maybe try to reconnect and not clear the suscribers?
          unsuscribeAll();
          if (e.wasClean) {
            /*log.debug(
              `Connection with ${address} closed, all suscribers cleared`
            );*/
            console.log(`Connection with ${address} closed, all suscribers cleared`);
          } else {
            //log.debug(`Connection with ${address} interrupted`);
            console.log(`Connection with ${address} interrupted`);
          }
        };
  
        websocket.onerror = (e) => {
          //log.debug(`Error received from websocket: ${e.type}`);
          console.log(`Error received from websocket: ${e.type}`)
          //reject();
        };
  
        websocket.onmessage = (e) => {
          const message = JSON.parse(e.data);
          dispatch(message);
          received_msg(message);
        };
      });
    };
  
    const send = (message, data) => {
      // Sending messages to remote manager
      return new Promise((resolve, reject) => {
        //const id = uuidv4();
        actual_id ++;
        const id = actual_id;
  
        if (!websocket) {
          reject({
            id: "",
            command: "error",
            data: {
              message: "Websocket not connected",
            },
          });
        }
  
        subscribeOnce(["ack", "error"], (response) => {
          if (id === response.id) {
            if (response.command === "ack") {
              console.log("RESOLVE SEND");
              resolve(response);
            } else {
              console.log("REJECT SEND");
              reject(response);
            }
          }
        });
  
        const msg = JSON.stringify({
          id: id,
          command: message,
          data: data,
        });
        websocket.send(msg);
      });
    };
  
    // Messages and events
    const commands = {
      connect: connect,
      launch: (configuration) => send("launch", configuration),
      run: () => send("run"),
      stop: () => send("stop"),
      pause: () => send("pause"),
      resume: () => send("resume"),
      reset: () => send("reset"),
      terminate: () => send("terminate"),
      disconnect: () => send("disconnect"),
    };
  
    return {
      ...commands,
  
      send: send,
  
      events: events,
      subscribe: subscribe,
      unsubscribe: unsubscribe,
      suscribreOnce: subscribeOnce,
    };
  };
  
  window.RoboticsExerciseComponents = (function() {
      const ramHost = window.location.hostname;
      const ramPort = 7163;
      const ramManager = CommsManager(`ws://${ramHost}:${ramPort}`);
    
      return {
        commsManager: ramManager
      }
  
  })()

  window.addEventListener("DOMContentLoaded", () => {
    // Open the WebSocket connection and register event handlers.
    window.RoboticsExerciseComponents.commsManager.connect();
    
    button_pressed("btn_launch");

    catch_file();
    button_pressed("btn_term");
    button_pressed("btn_con");
    button_pressed("btn_run");
    button_pressed("btn_stp");
    button_pressed("btn_pause");
    button_pressed("btn_resume");
    button_pressed("btn_disc");
    button_pressed("btn_load");
    button_pressed("views");
  });

  function received_msg(message) {
    console.log(message.command,message.data);

    if (message.command === "ack") {
      switch (message.data){
        case "stop":
        case "launch":
        case "load":
          // estoy en READY
          document.getElementById('btn_launch').style.display = 'none';
          document.getElementById('btn_term').style.display = 'inline';
          document.getElementById('btn_con').style.display = 'none';
          document.getElementById('btn_run').style.display = 'inline';
          document.getElementById('btn_stp').style.display = 'none';
          document.getElementById('btn_pause').style.display = 'none';
          document.getElementById('btn_resume').style.display = 'none';
          document.getElementById('btn_disc').style.display = 'inline';
          document.getElementById('btn_load').style.display = 'inline';
		  document.getElementById("file-selector").style.display = 'inline';
          break;
        case "terminate":
        case "connect":
          // estoy en CONNECTED
          document.getElementById('btn_launch').style.display = 'inline';
          document.getElementById('btn_term').style.display = 'none';
          document.getElementById('btn_con').style.display = 'none';
          document.getElementById('btn_run').style.display = 'none';
          document.getElementById('btn_stp').style.display = 'none';
          document.getElementById('btn_pause').style.display = 'none';
          document.getElementById('btn_resume').style.display = 'none';
          document.getElementById('btn_disc').style.display = 'inline';
          document.getElementById('btn_load').style.display = 'none';
		  document.getElementById("file-selector").style.display = 'none';
            break;
        case "pause":
          // estoy en PAUSED
          document.getElementById('btn_launch').style.display = 'none';
          document.getElementById('btn_term').style.display = 'none';
          document.getElementById('btn_con').style.display = 'none';
          document.getElementById('btn_run').style.display = 'none';
          document.getElementById('btn_stp').style.display = 'inline';
          document.getElementById('btn_pause').style.display = 'none';
          document.getElementById('btn_resume').style.display = 'inline';
          document.getElementById('btn_disc').style.display = 'inline';
          document.getElementById('btn_load').style.display = 'inline';
		  document.getElementById("file-selector").style.display = 'inline';
            break;
        case "resume":
        case "run":
          // estoy en RUNNING
          document.getElementById('btn_launch').style.display = 'none';
          document.getElementById('btn_term').style.display = 'none';
          document.getElementById('btn_con').style.display = 'none';
          document.getElementById('btn_run').style.display = 'none';
          document.getElementById('btn_stp').style.display = 'inline';
          document.getElementById('btn_pause').style.display = 'inline';
          document.getElementById('btn_resume').style.display = 'none';
          document.getElementById('btn_disc').style.display = 'inline';
          document.getElementById('btn_load').style.display = 'inline';
		  document.getElementById("file-selector").style.display = 'inline';
            break;
        case "disconnect":
          // esto en IDLE
          document.getElementById('btn_launch').style.display = 'none';
          document.getElementById('btn_term').style.display = 'none';
          document.getElementById('btn_con').style.display ='inline';
          document.getElementById('btn_run').style.display = 'none';
          document.getElementById('btn_stp').style.display = 'none';
          document.getElementById('btn_pause').style.display = 'none';
          document.getElementById('btn_resume').style.display = 'none';
          document.getElementById('btn_disc').style.display = 'none';
          document.getElementById('btn_load').style.display = 'none';
		  document.getElementById("file-selector").style.display = 'none';
            break;
        default:
          document.getElementById('btn_launch').style.display = 'inline';
          document.getElementById('btn_term').style.display = 'inline';
          document.getElementById('btn_con').style.display ='inline';
          document.getElementById('btn_run').style.display = 'inline';
          document.getElementById('btn_stp').style.display = 'inline';
          document.getElementById('btn_pause').style.display = 'inline';
          document.getElementById('btn_resume').style.display = 'inline';
          document.getElementById('btn_disc').style.display = 'inline';
          document.getElementById('btn_load').style.display = 'inline';
		  document.getElementById("file-selector").style.display = 'inline';
      }
    }
    
  }

  function loadPages(){
	console.log("GZ")
	var frame = $('#gz-vnc');
	var url = 'http://127.0.0.1:6080/vnc.html?resize=remote&amp;autoconnect=true';
    frame.attr('src',url).show();

	console.log("CONSOLE")
	frame = $('#console-vnc')
	url = 'http://127.0.0.1:1108/vnc.html?resize=remote&amp;autoconnect=true'
	frame.attr('src',url).show();

	console.log("RVIZ")
	frame = $('#rviz-vnc')
	url = 'http://127.0.0.1:6081/vnc.html?resize=remote&amp;autoconnect=true'
	frame.attr('src',url).show();

	console.log("GUI")
	frame = $('#gui-vnc')
	url = 'http://127.0.0.1:6082/vnc.html?resize=remote&amp;autoconnect=true'
	frame.attr('src',url).show();
}
  
  function button_pressed(button) {

    switch (button){
        case "btn_launch":
            var comand = "launch";
            break;
        case "btn_term":
            var comand = "terminate"; 
            break;
        case "btn_stp":
            var comand = "stop"; 
            break;
        case "btn_pause":
            var comand = "pause"; 
            break;
        case "btn_resume":
            var comand = "resume"; 
            break;
        case "btn_disc":
            var comand = "disconnect"; 
            break;
        case "btn_run":
            var comand = "run"; 
            break;
        case "btn_con":
            var comand = "connect"; 
            break;
        case "btn_load":
            var comand = "load";
            break;
        case "views":
			document.getElementById(button).addEventListener("click",e=> {
				console.log("views");
				loadPages();})
          return;
        default:
          return;
    }
  
      document.getElementById(button).addEventListener("click",e=>{
        if (comand === "launch") {
            fetch('./configuration.json')
                .then((response) => response.json())
                .then((json)=> {
                    console.log(json);
                    console.log(comand);
                    window.RoboticsExerciseComponents.commsManager.send(comand,json);
                })
        } else if (comand === "load") {
            if (fileContent_loaded) {
              window.RoboticsExerciseComponents.commsManager.send(comand,fileContent);
            } else {
              return;
            }
        } else {
            window.RoboticsExerciseComponents.commsManager.send(comand);
        }
        
    })
  }
  
  function catch_file(){
    // Obtener el elemento de entrada de archivo
    const inputElement = document.getElementById("file-selector");
    
    // Cuando se selecciona un archivo, leer su contenido
    inputElement.addEventListener("change", (event) => {
      
        const file = event.target.files[0];
        const reader = new FileReader();
        //reader.readAsArrayBuffer(file);
        reader.readAsText(file);
  
    
        // Cuando se termine de cargar el archivo, obtener su contenido como cadena
        reader.onload = (event) => {
            fileContent = event.target.result;
            console.log(fileContent); // muestra el contenido del archivo en la consola
            window.RoboticsExerciseComponents.commsManager.send("load",fileContent);
            fileContent_loaded = true;
        };
        
    });
  }