import socket
import json
from os import getcwd
import sys

from bge import logic, events

with open(getcwd() + "\\Scripts\\Network\\network_config.json") as file:
    network_config = json.load(file)


class Lobby:
    def __init__(self, name):
        scene = logic.getCurrentScene()
        self.message = scene.objects['message_{}'.format(name)]

        self.manager_ip = network_config['manager_ip']
        self.manager_port = 9998
        self.manager_ip_port = "{}:{}".format(self.manager_ip, self.manager_port)

        self.connected = self.connect()

        self.manager = ""
        self.connect()

        self.ip = ""
        self.port = ""

    def connect(self):
        try:
            self.manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.manager.connect((self.manager_ip, self.manager_port))
            self.manager.settimeout(5)
            return True
        except:
            self.message.text = "It looks like the servers are down\n" \
                                "Please try again later"
            self.message.color = [255, 0, 0, 1]
            return False
