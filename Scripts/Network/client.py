import socket
import threading
from bge import logic, events
from mathutils import Vector, Euler
import json
import requests
import threading
from os import getcwd
from random import randint
from Network.packet_handler import PacketHandler


def keyDown(key_code=events.WKEY, status=logic.KX_INPUT_ACTIVE):
    """
    This method checks if the key (key_code) is active
    i.e. keyDown(events.WKEY) checks if the w_key is being pressed
    """
    if logic.keyboard.events[key_code] == status:
        return True
    return False


with open(getcwd() + "\\Scripts\\Network\\network_config.json") as file:
    network_config = json.load(file)


class Client:
    def __init__(self, ip, port):
        """" Initialize the client """

        self.packet_handler = None
        logic.globalDict['TestMode'] = False

        # The color of the enemy
        self.enemy_color = [0.5, 0, 0, 0.2]
        # set True if player is the host of the server

        self.host = logic.globalDict['host']

        self.config = []

        # Set this to True if you run it locally and to False if you run it on a server
        self.local = network_config['local']

        # Here we store what player belongs to this instance of the client
        self.user_initialized = False
        self.user = []

        if not self.local:
            self.ip = requests.get("http://ipecho.net/plain?").text
        else:
            self.ip = "127.0.0.1"  # YOUR IP HERE

        print(self.ip)

        # Connect to the server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('', 0))
        self.server.setblocking(False)

        print("[i] connected to server")

        self.port = self.server.getsockname()[1]

        # The IP & Port of the server
        self.server_ip = ip  # IP FROM THE PLACE WHERE YOU ARE RUNNING THE SERVER ON HERE
        self.server_port = port

        self.server_ip_port = (self.server_ip, self.server_port)

        # Here we store the player objects (the tanks)
        # So we can move it in the scene and get the world positions
        self.players = {}

        self.oldpos = {}

        i_am_new = json.dumps({"i am new": (self.ip, self.port)}).encode()
        self.server.sendto(i_am_new, self.server_ip_port)

    def worldpos(self):
        """" Send the worldposition of the player object to the server """
        try:
            player = self.players["{}:{}".format(self.ip, self.port)]['instance']
            pos = [list(player.worldPosition), player.localOrientation.to_euler()[2]]
            if self.oldpos != pos:
                key_stat = {
                    'position': {
                        'coordinates': pos,
                        'ip': "{}:{}".format(self.ip, self.port)
                    }
                }
                self.oldpos = [list(player.worldPosition), player.localOrientation.to_euler()[2]]
                self.server.sendto(json.dumps(key_stat).encode(), self.server_ip_port)
        except:
            pass
            # print("erro")
            # not initialized yet

    def shoot(self):
        # shooting for the tank player
        keyboard = logic.keyboard
        JUST_ACTIVATED = logic.KX_INPUT_JUST_ACTIVATED

        # self.local_user
        cannon = self.local_user.children[0]
        scene = logic.getCurrentScene()
        master = scene.objects['MASTER']
        sh = master.sensors['Shoot']
        shoot = keyDown(logic.globalDict['key_binding']['shoot'])

        if self.local_user['PartyMode'] == True or logic.globalDict['PartyModeForEver']:
            if shoot or sh.positive:
                bullet = scene.addObject("Bullet", cannon, 20)
                bullet['team'] = self.local_user['team']

                # In deze json zet je de details van wat er moet gebeuren
                # (net zoals bij het position pakketje stop je er de coordinaten in)
                shoot = {
                    'shoot': {
                        'ip': "{}:{}".format(self.ip, self.port),
                        'team': self.local_user['team']
                    }
                }

                # Stuur het naar de server
                self.server.sendto(json.dumps(shoot).encode(), self.server_ip_port)
        else:
            if keyboard.events[logic.globalDict['key_binding']['shoot']] == JUST_ACTIVATED:
                bullet = scene.addObject("Bullet", cannon, 20)
                bullet['team'] = self.local_user['team']

                # In deze json zet je de details van wat er moet gebeuren
                # (net zoals bij het position pakketje stop je er de coordinaten in)
                shoot = {
                    'shoot': {
                        'ip': "{}:{}".format(self.ip, self.port),
                        'team': self.local_user['team']
                    }
                }

                # Stuur het naar de server
                self.server.sendto(json.dumps(shoot).encode(), self.server_ip_port)

                print("FIRE")

    def cshoot(self):
        scene = logic.getCurrentScene()
        cannon = self.local_user.children[0]

        bullet = scene.addObject("Bullet", cannon, 20)
        bullet['team'] = self.local_user['team']

        # In deze json zet je de details van wat er moet gebeuren
        # (net zoals bij het position pakketje stop je er de coordinaten in)
        shoot = {
            'shoot': {
                'ip': "{}:{}".format(self.ip, self.port),
                'team': self.local_user['team']
            }
        }

        # Stuur het naar de server
        self.server.sendto(json.dumps(shoot).encode(), self.server_ip_port)

    def receive(self):
        """"
        Receive all the packets from the server.
        Check what kind of packet it is: movement? new connection?
        and handle the packet
        """
        for i in range(10):
            try:
                # Listen for incoming packets
                data, addr = self.server.recvfrom(1024)
                handler = threading.Thread(target=self.packet_handler.handle_packet, args=(json.loads(data.decode()),))
                handler.start()
            except socket.error:
                pass

    def respawn(self):
        # get the controller
        controller = logic.getCurrentController()
        # get object that controller is attached to
        obj = controller.owner
        scene = logic.getCurrentScene()
        gameScene = logic.getSceneList()[0]
        for key in self.players.keys():
            if self.players[key]['instance'] == obj:
                team = self.players[key]['team']
                if team == 'team1':
                    point = randint(1, 2)
                    spawner = scene.objects["Spawner{}".format(point)]
                    if point == 1:
                        euler = [0, 0, 0.1]
                    else:
                        euler = [0, 0, -3]
                else:
                    point = randint(3, 4)
                    spawner = scene.objects["Spawner{}".format(point)]
                    if point == 3:
                        euler = [0, 0, -3]
                    else:
                        euler = [0, 0, 0.1]
        # set object's world position
        obj.worldPosition = spawner.worldPosition
        obj.localOrientation = euler

    def getPlayers(self):
        testMode = logic.globalDict['TestMode']
        if not testMode:
            logic.globalDict['numOfPlayers'] = len(self.players)
            if len(self.players) >= 2:
                hud = logic.getSceneList()[-1]
                Waiting = hud.objects['Waiting']
                Waiting['visible'] = False
        else:
            logic.globalDict['numOfPlayers'] = 20
            hud = logic.getSceneList()[-1]
            Waiting = hud.objects['Waiting']
            Waiting['visible'] = False


if network_config['server_manager']:
    client = Client(logic.globalDict['ip'], logic.globalDict['port'])
else:
    if __name__ == "client":
        logic.globalDict['host'] = False
        client = Client(network_config['server_ip'], 9999)
    else:
        client = None

client.packet_handler = PacketHandler(client)


def movement():
    if client.user_initialized:
        client.movement(client.local_user)


def sendworldpos():
    client.worldpos()


def receive():
    client.receive()


def shoot():
    if client.user_initialized:
        client.shoot()


def respawn():
    client.respawn()


def getlocaluser():
    return client.local_user


def contShoot():
    joystick = logic.joysticks[0]
    btns = joystick.activeButtons

    scene = logic.getCurrentScene()
    master = scene.objects['MASTER']
    sh = master.sensors['Shoot']

    if sh.positive and 2 in btns:
        client.cshoot()


def numOfPlay():
    client.getPlayers()
