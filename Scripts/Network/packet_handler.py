from random import randint
from bge import logic
from os import getcwd
from mathutils import Vector, Euler

import configparser


class PacketHandler:
    def __init__(self, client):
        self.client = client

    def handle_packet(self, packet):
        if 'ping' in packet.keys():
            print(packet['ping'])
            self.client.server.sendto(b'pong', self.client.server_ip_port)
        elif 'new-connection' in packet.keys():
            """"
            A new client has connected to the server
            We spawn it on the client's game so he can see it too
            We the player under the IP of the new client so we can apply movement on it later
            """

            # Ip of the new client
            ip = packet['new-connection']['ip']

            # What is the name of the object the client has?
            # Might be usefull for upgrades ect..
            object = packet['new-connection']['object']

            # Get the current scene and spawn the client in the spawner
            team = packet['new-connection']['team']
            scene = logic.getCurrentScene()
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

            player = scene.addObject(object, spawner)
            player.localOrientation = euler
            player["ip"] = ip
            player["team"] = packet['new-connection']['team']

            # Add the ip to the player object

            self.client.players[ip] = {}
            self.client.players[ip]['instance'] = player

            self.client.players[ip]['team'] = team

            # If it is the first time a user is "intitialized" then we know that this is
            # the user that belongs to this self.client. So we store the object
            if not self.client.user_initialized:
                logic.globalDict['matches'] = packet['new-connection']['matches']
                print(packet['new-connection']['matches'])
                logic.globalDict['current_match'] = 0
                self.client.local_user = player
                self.client.local_user['team'] = team
                # Color all the tanks
                scene = logic.getCurrentScene()
                for object in scene.objects:
                    if object.name == "Tank":
                        print(object['team'])
                        print(team)
                        if object['team'] != team:
                            object.color = self.client.enemy_color

                self.client.user_initialized = True
                print(self.client.local_user.children)
                logic.globalDict['local_user'] = player

                configParser = configparser.RawConfigParser()
                cfp = getcwd() + "\Config\TankConfig.txt"
                configParser.read(cfp)

                if self.client.host is True:
                    print(logic.globalDict)
                    player['MovementSpeed'] = (logic.globalDict["MovementSpeed"] / 1000)
                    if logic.globalDict['TurtleMode'] is True:
                        player['HitPoints'] = (logic.globalDict["HitPoints"] * 1000)
                    else:
                        player['HitPoints'] = logic.globalDict["HitPoints"]
                    player['FirePower'] = logic.globalDict["FirePower"]

                else:
                    if not 'config' in logic.globalDict.keys():
                        self.client.config = packet['new-connection']['config']
                        config = [
                            "PartyModeTTL",
                            "ExtraHullTTL",
                            "SpeedBoostTTL",
                            "PartyModeChance",
                            "ExtraHullChance",
                            "SpeedBoostChance",
                            "MovementSpeed",
                            "HitPoints",
                            "FirePower",
                            "JumpingPowerUp",
                            "PartyModeForEver",
                            "TurtleMode"
                        ]

                        print("^^^^^^^^^^^^^^^^^^^^^^^^^")
                        print(self.client.config)
                        print("^^^^^^^^^^^^^^^^^^^^^^^^^")

                        try:
                            configlist = self.client.config['config']
                            for i, y in enumerate(configlist):
                                logic.globalDict[config[i]] = configlist[i]
                            self.client.local_user['MovementSpeed'] = (logic.globalDict['MovementSpeed'] / 1000)
                            if logic.globalDict['TurtleMode'] is True:
                                player['HitPoints'] = (logic.globalDict["HitPoints"] * 1000)
                            else:
                                player['HitPoints'] = logic.globalDict["HitPoints"]
                            self.client.local_user['FirePower'] = logic.globalDict['FirePower']
                        except:
                            "Error in config list"
            else:
                if team != self.client.local_user['team']:
                    player.color = self.client.enemy_color

        elif 'init_connection' in packet.keys():
            """" 
            if a user connects to the server and there are allready other players inside the game
            then we need to get the information about the other objects so we can spawn them in ect..
            """
            scene = logic.getCurrentScene()
            initialized = {
                gobj["ip"]: [list(gobj.worldPosition), gobj.localOrientation.to_euler()[2]] \
                for gobj in scene.objects \
                if gobj.name == "Tank"
            }

            if not len(initialized):
                for event in packet['init_connection']:
                    scene = logic.getCurrentScene()

                    tank = 'Tank'

                    self.client.players[event] = {}
                    print(packet['init_connection'])
                    team = packet['init_connection'][event]['team']
                    self.client.players[event]['team'] = team
                    # get spawner according to team
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

                    player = scene.addObject(tank, spawner)
                    player['ip'] = event
                    player['team'] = team
                    self.client.players[event]['instance'] = player

                    # Handle the rotation
                    # We use Eueler for this (the last number handles the Z rotation)
                    player.localOrientation = [0, 0, packet['init_connection'][event]['position'][1]]

                    # Change the players position to the given position
                    # We us a vecor for this
                    player.worldPosition = Vector(packet['init_connection'][event]['position'][0])

        elif 'position' in packet.keys():
            """" 
            These packets contain the position (worldlocation & rotation) of a specific player
            if the ip in the packet is not equal to the clients IP then apply the movement
            (otherwise this will override the movement and the player would be stuck on one position)
            """
            try:
                for event in packet['position']:
                    if self.client.user_initialized and event \
                            != "{}:{}".format(self.client.ip, self.client.port):
                        # Get the object that belongs to that ip
                        instance = self.client.players[event]['instance']

                        # Handle the rotation
                        instance.localOrientation = [0, 0, packet['position'][event][1]]

                        # Handle the movement
                        instance.worldPosition = Vector(packet['position'][event][0])
            except:
                # NOTE: it's possible that this packet came in before we initialized the objects
                # so it can probably not find the right object. So no worries about this error
                print("Something went wrong handling the position. Line: 150")

        elif 'shoot' in packet.keys():
            """"
            Handle the shooting packet
            """
            try:
                ip = packet['shoot']['ip']
                if ip != "{}:{}".format(self.client.ip, self.client.port):
                    instance = self.client.players[ip]['instance']
                    cannon = instance.children[0]
                    scene = logic.getCurrentScene()
                    bullet = scene.addObject("Bullet", cannon, 20)
                    bullet['team'] = packet['shoot']['team']
            except:
                pass

        elif 'disconnect' in packet.keys():
            try:
                ip = packet['disconnect']['ip']
                instance = self.client.players[ip]['instance']
                instance.endObject()
                self.client.players.pop(ip)
            except:
                pass
        elif 'powerup_spawn' in packet.keys():
            logic.globalDict['RandomNumber'] = packet['powerup_spawn']
            # print(packet['powerup_spawn'])
