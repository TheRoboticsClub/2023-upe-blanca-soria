// Main message controller for websockets
var running = true;
var resetRequested = false;
var firstCodeSent = false;

// Function to execute the student solution
function start(){
    enablePlayPause(false);
    toggleResetButton(false);

    // Manager Websocket
    if (running == false) {
        resumeSimulation();
        resumeBrain();
    }

    // Code Websocket
    togglePlayPause(true);
    running = true;
}

function check() {
    toggleSubmitButton(false);
    toggleResetButton(false);
    checkCode();
}

// Function to stop the student solution
function stop(){
    enablePlayPause(false);
    toggleResetButton(false);

    // Manager Websocket
    if (running == true) {
        stopSimulation();
        stopBrain();
    }

    togglePlayPause(false);
    running = false;
}

// Function to reset the simulation
function resetSim(){
    // Manager Websocket
    resetRequested = true;
    enablePlayPause(false);
    togglePlayPause(false);
    toggleResetButton(false);
    toggleSubmitButton(false);
    resetSimulation();
    firstCodeSent = false;
    running = false;
}

function enableSimControls() {
    if (!resetRequested)
        stop();
    togglePlayPause(false);
    let reset_button = document.getElementById("reset");
    reset_button.disabled = false;
    reset_button.style.opacity = "1.0";
    reset_button.style.cursor = "default";
    let load_button = document.getElementById("loadIntoRobot");
    load_button.disabled = false;
    load_button.style.opacity = "1.0";
    load_button.style.cursor = "default";
    console.log(load_button.disabled);
}