from typing import Any
import time

from src.libs.process_utils import get_class, class_from_module
from src.ram_logging.log_manager import LogManager
from src.manager.vnc.console_view import Console_view
from src.manager.vnc.gzb_view import Gzb_view
from src.manager.vnc.rviz_view import Rviz_view
from src.manager.vnc.docker_thread import DockerThread
import subprocess

class Launcher:

    def __init__(self, exercise):
        self.exercise = exercise
        self.gzb_viewer = Gzb_view(":0", 5900, 6080)
        self.console_viewer = Console_view(":1", 5901, 1108)
        self.rviz_viewer = Rviz_view(":2",5902,6081)

    def run(self):
        self.console_viewer.start_console(1920, 1080)

        exercise_launch_cmd = f"DISPLAY=:0 ros2 launch {self.exercise} spawn_model.launch.py"
        exercise_launch_thread = DockerThread(exercise_launch_cmd)
        exercise_launch_thread.start()
        print(f"\nstarted launch exercise: {self.exercise} thread\n")

        gazebo_launch_cmd = "DISPLAY=:0 ros2 launch gazebo_ros gazebo.launch.py"
        gazebo_thread = DockerThread(gazebo_launch_cmd)
        gazebo_thread.start()
        print("\nstarted launch gazebo thread\n")

        self.rviz_viewer.start_rviz()

    def terminate(self):
        kill_cmd = 'pkill -9 -f '
        cmd = kill_cmd +'rviz'
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1024, universal_newlines=True)
        cmd = kill_cmd + 'gzclient'
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1024, universal_newlines=True)
        cmd = kill_cmd + 'gzserver'
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1024, universal_newlines=True)
        cmd = kill_cmd + 'xterm'
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1024, universal_newlines=True)
        cmd = kill_cmd + 'websockify'
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1024, universal_newlines=True)
        cmd = kill_cmd + 'xorg'
        subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1024, universal_newlines=True)

        
        
