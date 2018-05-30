import socket
import json
from Scripts.Menu.lobby import Lobby

from bge import logic, events


class HostingLobby(Lobby):
    def __init__(self):
        super().__init__('host')
        self.host_clicked = False

    def handler(self):
        if not self.host_clicked:
            if not self.connected:
                self.connected = self.connect()
            if self.connected:
                self.host_clicked = True
                host_server = {
                    'host_server': {
                        'config': logic.globalDict['configlist'],
                    }
                }
                self.manager.sendall(json.dumps(host_server).encode())
                try:
                    self.manager.settimeout(5)
                    print('hi')
                    packet = self.manager.recv(10024)
                    print(packet)
                    packet = json.loads(packet.decode())
                    if "allready_hosting" in packet.keys():
                        dns = packet['allready_hosting']
                        self.message.text = "You are allready hosting a server your server id\n" \
                                            "is stated below"
                        self.message.color = [255, 0, 0, 1]
                    elif "server_full" in packet.keys():
                        self.message.text = "The server is full please try again later!"
                        self.message.color = [255, 0, 0, 1]
                    else:
                        dns = packet['dns']
                        logic.globalDict['dns'] = dns
                        logic.globalDict['host'] = True
                        self.ip = packet['ip']
                        self.port = int(packet['port'])
                        for scene in logic.getSceneList():
                            if scene.name == 'HostScene':
                                logic.globalDict['ip'] = self.ip
                                logic.globalDict['port'] = self.port
                                logic.globalDict['host'] = True
                                scene.replace('Game')
                except socket.error:
                    self.message.text = "It looks like the servers are down\n" \
                                        "Please try again later"
                    self.message.color = [255, 0, 0, 1]
            self.host_clicked = False


handler = HostingLobby()


def handle():
    handler.handler()
