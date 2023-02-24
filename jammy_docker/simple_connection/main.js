
window.addEventListener("DOMContentLoaded", () => {
    // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:8001/");
    catch_file(websocket);
    button_pressed("btn_load",websocket);
    button_pressed("btn_launch",websocket);
    button_pressed("btn_term",websocket);
    button_pressed("btn_con",websocket);
    button_pressed("btn_run",websocket);
    button_pressed("btn_stp",websocket);
    button_pressed("btn_pause",websocket);
    button_pressed("btn_resume",websocket);
    button_pressed("btn_disc",websocket);

  });

function button_pressed(button,websocket) {

    switch (button){
        case "btn_load":
            var comand = "load"; 
            break;
        case "btn_launch":
            var comand = "launch"; 
            break;
        case "btn_term":
            var comand = "termiante"; 
            break;
        case "btn_con":
            var comand = "connect"; 
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
        default:
            var comand="";
    }

    document.getElementById(button).addEventListener("click",e=>{
        const ev = {
            id: "1",
            cmd: comand,
            data: "",
        };
        websocket.send(JSON.stringify(ev));
        //window.setTimeout(() => window.alert(comand), 50);
        console.log(ev);
    })
  }

function catch_file(websocket){
    // Obtener el elemento de entrada de archivo
    const inputElement = document.getElementById("file-selector");
    
    // Cuando se selecciona un archivo, leer su contenido
    inputElement.addEventListener("change", (event) => {
      
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.readAsArrayBuffer(file);
    
        // Cuando se termine de cargar el archivo, obtener su contenido como cadena
        reader.onload = (event) => {
            const fileContent = event.target.result;
            console.log(fileContent); // muestra el contenido del archivo en la consola
            websocket.send(fileContent);
        };
    });
}
