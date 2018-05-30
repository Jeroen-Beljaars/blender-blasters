from bge import logic
import json
from Scripts.Menu.lobby import Lobby


class JoiningLobby(Lobby):
    def __init__(self):
        super().__init__('join')
        cont = logic.getCurrentController()
        sens = cont.sensors['Message']
        self.input = sens.bodies
        self.active = False

    def handle(self):
        if not self.active:
            self.active = True
            scene = logic.getCurrentScene()
            cont = logic.getCurrentController()
            sens = cont.sensors['Message']
            self.input = sens.bodies
            senss = cont.sensors['Always']
            try:
                dns = self.input[0]  # can be changed to whatever just a variable to currently hold it in
            except:
                try:
                    dns = scene.objects['IPInputJoin'].text
                except:
                    dns = "None"
            print(self.input)
            print(dns)

            if not self.connected:
                self.connected = self.connect()
            if self.connected:
                try:
                    self.manager.sendall(json.dumps({"join": dns.upper()}).encode())
                    response = self.manager.recv(1024)
                    response = json.loads(response.decode())
                except:
                    self.message = "It looks like the servers are down\n" \
                                   "Please try again later"
                if 'no_record' in response.keys():
                    self.message.text = "Oops I didn't find a server for this ID."
                    self.message.color = [255, 0, 0, 1]
                elif 'server_info' in response.keys():
                    logic.globalDict['host'] = False
                    logic.globalDict['dns'] = dns
                    for scene in logic.getSceneList():
                        if scene.name == 'JoinScene':
                            logic.globalDict['ip'] = response['server_info']['ip']
                            logic.globalDict['port'] = response['server_info']['port']
                            scene.replace('Game')
                            break

handler = JoiningLobby()


def handle():
    handler.handle()
