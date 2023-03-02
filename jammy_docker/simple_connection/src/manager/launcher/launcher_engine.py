from typing import Any

from pydantic import BaseModel

from src.libs.process_utils import get_class, class_from_module
from src.ram_logging.log_manager import LogManager


class LauncherEngine(BaseModel):
    exercise_id: str
    launch: dict

    module = '.'.join(__name__.split('.')[:-1])
    terminated_callback: Any = None

    def run(self):
        keys = sorted(self.launch.keys())
        for key in keys:
            launcher_data = self.launch[key]
            launcher_type = launcher_data['type']
            print("<launcher_engine.py:run():1>--> launcher_data:",launcher_data," launcher_type:",launcher_type)

            # extend launcher data with
            # TODO: Review, maybe there's a better way to do this
            launcher_data["exercise_id"] = self.exercise_id
            print("<launcher_engine.py:run()>:2--> launcher_data:",launcher_data)

            if launcher_type == "module":
                launcher = self.launch_module(launcher_data)
                self.launch[key]['launcher'] = launcher
                print("<launcher_engine.py:run()>:3--> launch[",key,"]['launcher']:",launcher)
            elif launcher_type == "command":
                self.launch_command(launcher_data)
            else:
                print("<launcher_engine.py:run()>:4--> ",f"Launcher type {launcher_type} not valid")
                raise LauncherEngineException(f"Launcher type {launcher_type} not valid")

    def terminate(self):
        keys = sorted(self.launch.keys())
        for key in keys:
            launcher_data = self.launch[key]
            launcher_class = launcher_data.get('launcher', None)
            LogManager.logger.info(f"Terminating {key}")
            if launcher_class is not None and launcher_class.is_running():
                launcher_class.terminate()

    def launch_module(self, configuration):
        def process_terminated(name, exit_code):
            # LogManager.logger.info(f"LauncherEngine: {name} exited with code {exit_code}")
            print(f"\nLauncherEngine: {name} exited with code {exit_code}\n")
            if self.terminated_callback is not None:
                self.terminated_callback(name, exit_code)

        launcher_module_name = configuration["module"]
        print(f"<launcher_engine.py:launch_module(conf)>:1--> launcher_module_name:{launcher_module_name}")
        launcher_module = f"{self.module}.launcher_{launcher_module_name}.Launcher{class_from_module(launcher_module_name)}"
        print(f"<launcher_engine.py:launch_module(conf)>:2--> launcher_module:{launcher_module}")
        #launcher_class = get_class(launcher_module)
        print(f"<launcher_engine.py:launch_module(conf)>:3--> launcher_class:{launcher_class}")
        #launcher = launcher_class.from_config(launcher_class, configuration)
        print(f"<launcher_engine.py:launch_module(conf)>:4--> launcher:{launcher}")
        #launcher.run(process_terminated)
        print("<launcher_engine.py:launch_module(conf)>:5--> launcher.run(callback)")
        #return launcher
        return ""

    def launch_command(self, configuration):
        pass


class LauncherEngineException(Exception):
    def __init__(self, message):
        super(LauncherEngineException, self).__init__(message)
