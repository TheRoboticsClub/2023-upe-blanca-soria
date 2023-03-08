from src.manager.vnc.vnc_server import Vnc_server
from src.manager.vnc.docker_thread import DockerThread
import subprocess

class Gui_view(Vnc_server):
    def __init__(self, display, internal_port, external_port):
        super().start_vnc(display, internal_port, external_port)
        self.display = display