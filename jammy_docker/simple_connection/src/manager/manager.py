from __future__ import annotations

import os
import time
import traceback
from queue import Queue
from uuid import uuid4
from src.manager.vnc.docker_thread import DockerThread
from transitions import Machine
from src.ram_logging.log_manager import LogManager
from src.comms.consumer_message import ManagerConsumerMessageException
from src.libs.process_utils import get_class, get_class_from_file
from src.manager.application.robotics_python_application_interface import IRoboticsPythonApplication
from src.manager.launcher.launcher import Launcher
from src.manager.lint.linter import Lint

import json


class Manager:
    states = [
        "idle",
        "connected",
        "ready",
        "running",
        "paused"
    ]

    transitions = [
        # Transitions for state idle
        {'trigger': 'connect', 'source': 'idle', 'dest': 'connected', },
        # Transitions for state connected
        {'trigger': 'launch', 'source': 'connected', 'dest': 'ready', 'before': 'on_launch'},
        # Transitions for state ready
        {'trigger': 'terminate', 'source': 'ready', 'dest': 'connected', 'before': 'on_terminate'},
        {'trigger': 'load', 'source': ['ready', 'running', 'paused'], 'dest': 'ready', 'before': 'load_code'},
        {'trigger': 'run', 'source': 'ready', 'dest': 'running', 'conditions': 'code_loaded', 'after': 'on_run'},
        # Transitions for state running
        {'trigger': 'stop', 'source': ['running', 'paused'], 'dest': 'ready', 'before': 'on_stop'},
        {'trigger': 'pause', 'source': 'running', 'dest': 'paused', 'before': 'on_pause'},
        # Transitions for state paused
        {'trigger': 'resume', 'source': 'paused', 'dest': 'running', 'before': 'on_resume'},
        # Global transitions
        {'trigger': 'disconnect', 'source': '*', 'dest': 'idle' , 'before': 'on_disconnect'}
    ]

    def __init__(self, host: str, port: int):
        self.__code_loaded = False
        self.exercise_id = None
        self.machine = Machine(model=self, states=Manager.states, transitions=Manager.transitions,
                               initial='idle', send_event=True, after_state_change=self.state_change)
        from src.comms.new_consumer import ManagerConsumer

        self.queue = Queue()

        # TODO: review, hardcoded values
        self.consumer = ManagerConsumer(host, port, self.queue)
        self.launcher = None
        self.application: IRoboticsPythonApplication = None
        self.linter = None

    def state_change(self, event):

        # LogManager.logger.info(f"State changed to {self.state}")
        print(f"\nState changed to {self.state}\n")

        if self.consumer is not None:
            self.consumer.send_message({'state': self.state}, command="state-changed")

    def update(self, data):
        #LogManager.logger.debug(f"Sending update to client")
        #print(f"\nSending update to client\n")
        if self.consumer is not None:
            self.consumer.send_message({'update': data}, command="update")

    def on_launch(self, event):
        """
        Transition executed on launch trigger activ
        """
        def terminated_callback(name, code):
            # TODO: Prototype, review this callback

            # LogManager.logger.info(f"Manager: Launcher {name} died with code {code}")
            print(f"\nManager: Launcher {name} died with code {code}\n")

            if self.state != 'ready':
                self.terminate()

        configuration = event.kwargs.get('data', {})

        # generate exercise_folder environment variable
        self.exercise_id = configuration['exercise_id']
        os.environ["EXERCISE_FOLDER"] = f"{os.environ.get('EXERCISES_STATIC_FILES')}/{self.exercise_id}"
        self.linter = Lint(self.exercise_id)

        # Check if application and launchers configuration is missing
        # TODO: Maybe encapsulate configuration as a data class with validation?
        print("\nloading configuration of the application\n")
        application_configuration = configuration.get('application', None)
        if application_configuration is None:
            print("error with application configuration")
            raise Exception("Application configuration missing")

        
        # check if launchers configuration is missing
        print("\nloading configuration of launcher\n")
        launchers_configuration = configuration.get('launch', None)
        if launchers_configuration is None:
            print("error with launcher configuration")
            raise Exception("Launch configuration missing")

        # LogManager.logger.info(f"Launch transition started, configuration: {configuration}")
        print(f"\nLaunch transition started, configuration: {configuration}\n")

        #configuration['terminated_callback'] = terminated_callback
        self.launcher = Launcher(self.exercise_id)
        self.launcher.run()

        # TODO: launch application
        print("\nstarting Application\n")
        application_file = application_configuration['entry_point']
        params = application_configuration.get('params', None)
        application_module = os.path.expandvars(application_file)
        application_class = get_class_from_file(application_module, "Exercise")

        if not issubclass(application_class, IRoboticsPythonApplication):
            self.launcher.terminate()
            raise Exception("The application must be an instance of IRoboticsPythonApplication")

        params['update_callback'] = self.update
        self.application = application_class(**params)
        print("APPLICATION CREATED")

    def on_terminate(self, event):
        try:
            self.application.terminate()
            self.launcher.terminate()
        except Exception as e:
            #LogManager.logger.exception(f"Exception terminating instance")
            print(f"\nException terminating instance\n")
            print(traceback.format_exc())

    def on_enter_connected(self, event):
        # LogManager.logger.info("Connect state entered")
        print("\nConnect state entered\n")

    def on_enter_ready(self, event):
        configuration = event.kwargs.get('data', {})
        # LogManager.logger.info(f"Start state entered, configuration: {configuration}")
        print(f"\nStart state entered, configuration: {configuration}\n")

    def load_code(self, event):
        try:
            # LogManager.logger.info("Internal transition load_code executed")
            print("\nInternal transition load_code executed\n")

            message_data = event.kwargs.get('data', {})
            message_data = json.loads(message_data) # !!
            errors = self.linter.evaluate_code(message_data['code'])
            print(errors)

            if errors is "":
                #self.application.load_code(message_data['code'])
                print(f"\nself.application.load_code({message_data['code']})\n")
                self.__code_loaded = True
            else:
                raise Exception
        except Exception as e:
            self.__code_loaded = False
        
            self.consumer.send_message({'linter': errors}, command="linter")

    def code_loaded(self, event):
        return self.__code_loaded

    def process_messsage(self, message):
        last_state = self.state
        self.trigger(message.command, data=message.data or None)
        print("LAST STATE: ", last_state, "TRIGGER: ",message.command, "ACTUAL STATE: ", self.state,"CODE LOADED: ",self.__code_loaded)
        if (last_state != self.state):
            response = {"message": f"Exercise state changed to {self.state}"}
            self.consumer.send_message(message.response(response))
        else:
            exception_msg = f"couldnt change from state {last_state} to {message.command}"
            ex = ManagerConsumerMessageException(id=message.id, message=str(exception_msg))
            self.consumer.send_message(ex)
            print("\n",exception_msg,"\n")

    def on_run(self, event):
        # self.application.run()
        print("\non run\n")

    def on_pause(self, msg):
        #self.application.pause()
        print("\non pause\n")

    def on_resume(self, msg):
        #self.application.resume()
        print("\non resume\n")

    def on_stop(self, msg):
        #self.application.stop()
        print("\non stop\n")

    def on_disconnect(self, event):
        print("\non disconnect\n")
        if (self.state != "connected" and  self.state != "idle"):
            self.application.terminate()
            self.launcher.terminate()
        else:
            pass

    def start(self):
        """
        Starts the RAM
        RAM must be run in main thread to be able to handle signaling other processes, for instance ROS launcher.
        """
        # LogManager.logger.info(f"Starting RAM consumer in {self.consumer.server}:{self.consumer.port}")
        print(f"\nStarting RAM consumer in {self.consumer.server}:{self.consumer.port}\n")
       
        self.consumer.start()
        # TODO: change loop end condition
        while True:
            message = None
            try:
                if self.queue.empty():
                    time.sleep(0.1)
                else:
                    message = self.queue.get()
                    self.process_messsage(message)
            except Exception as e:
                if message is not None:
                    ex = ManagerConsumerMessageException(id=message.id, message=str(e))
                else:
                    ex = ManagerConsumerMessageException(id=str(uuid4()), message=str(e))
                self.consumer.send_message(ex)
                #LogManager.logger.error(e, exc_info=True)
                print(ex)
                

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str, help="Host to listen to  (0.0.0.0 or all hosts)")
    parser.add_argument("port", type=int, help="Port to listen to")
    args = parser.parse_args()

    RAM = Manager(args.host, args.port)
    RAM.start()
