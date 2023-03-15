import os
from typing import List, Any
import time

from src.manager.launcher.launcher_interface import ILauncher, LauncherException
from src.manager.docker_thread.docker_thread import DockerThread
import subprocess

import logging

class LauncherRosApi(ILauncher):
    exercise_id: str
    type: str
    module: str
    resource_folders: List[str]
    model_folders: List[str]
    plugin_folders: List[str]
    parameters: List[str]
    launch_file: str
    running = False

    def run(self,callback):
        logging.getLogger("roslaunch").setLevel(logging.CRITICAL)

        # expand variables in configuration paths
        self._set_environment()
        launch_file = os.path.expandvars(self.launch_file)

        #TODO: intruce correct path through launch configuration
        launch_file = '/RoboticsAcademy/exercises/static/exercises/follow_line_newmanager_ros2/web-template/launch/simple_line_follower_ros_headless_default.launch.py'
        
        exercise_launch_cmd = f"ros2 launch {launch_file}"
        exercise_launch_thread = DockerThread(exercise_launch_cmd)
        exercise_launch_thread.start()

        self.running = True

    def is_running(self):
        return self.running

    def terminate(self):
        if self.is_running():
            kill_cmd = 'pkill -9 -f '
            cmd = kill_cmd + 'gzserver'
            subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1024, universal_newlines=True)
            cmd = kill_cmd + 'spawn_model.launch.py'
            subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1024, universal_newlines=True)

    def _set_environment(self):
        #TODO: intruce correct path through launch configuration
        self.model_folders = ['$CUSTOM_ROBOTS_FOLDER/f1']

        resource_folders = [os.path.expandvars(path) for path in self.resource_folders]
        model_folders = [os.path.expandvars(path) for path in self.model_folders]
        plugin_folders = [os.path.expandvars(path) for path in self.plugin_folders]

        os.environ["GAZEBO_RESOURCE_PATH"] = f"{os.environ.get('GAZEBO_RESOURCE_PATH', '')}:{':'.join(resource_folders)}"
        os.environ["GAZEBO_MODEL_PATH"] = f"{os.environ.get('GAZEBO_MODEL_PATH', '')}:{':'.join(model_folders)}"
        os.environ["GAZEBO_PLUGIN_PATH"] = f"{os.environ.get('GAZEBO_PLUGIN_PATH', '')}:{':'.join(plugin_folders)}"