from src.manager.vnc.vnc_server import Vnc_server
from src.manager.vnc.docker_thread import DockerThread
import subprocess
import time

class Rviz_view(Vnc_server):
    def __init__(self, display, internal_port, external_port):
        super().start_vnc(display, internal_port, external_port)
        self.display = display

    def start_rviz(self):
        roslaunch_thread = DockerThread(f"DISPLAY={self.display} rviz2")
        roslaunch_thread.start()
