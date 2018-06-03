import socket
import json
from Scripts.Menu.lobby import Lobby
from re import search

from bge import logic, events


class HostingLobby(Lobby):
    def __init__(self):
        super().__init__('host')
        self.key_map = {
            48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8',
            57: '9', 147: '2', 148: '4', 149: '6', 150: '8', 151: '1', 152: '3', 153: '5',
            154: '7', 155: '9'
        }
        self.host_clicked = False
        self.amout_of_rounds = 3

    def handler(self):
        if not self.host_clicked:
            if not self.connected:
                self.connected = self.connect()
            if self.connected:
                scene = logic.getCurrentScene()
                try:
                    matches = int(scene.objects['number_of_matches'].text)
                    if matches % 2 == 0:
                        matches += 1
                except:
                    matches = 3

                self.host_clicked = True
                host_server = {
                    'host_server': {
                        'config': logic.globalDict['configlist'],
                        'matches': matches
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

    def key_press(self):
        scene = logic.getCurrentScene()
        output = scene.objects['number_of_matches']
        cont = logic.getCurrentController()
        own = cont.owner
        for event in own.sensors['Keyboard'].events:
            if event[1] == 1:
                if event[0] == 133:
                    output.text = output.text[0:-1]
                try:
                    if len(output.text) < 2:
                        output.text = str(output.text) + str(self.key_map[event[0]])
                except:
                    pass

handler = HostingLobby()


def handle():
    handler.handler()


def key_press():
    handler.key_press()