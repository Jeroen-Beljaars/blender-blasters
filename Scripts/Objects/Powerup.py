from bge import logic


class PowerUp:

    def __init__(self, name, TTL):
        self.player = logic.globalDict['local_user']
        self.name = name
        self.TTL = TTL
        self.hud = logic.getSceneList()[-1]
        self.PowerUpInfo = self.hud.objects['PowerUpName']

    def setTTL(self):
        self.player['Timer'] = self.TTL
        print(self.TTL)

    def activate(self):
        self.player['PWActive'] = True
        self.player['ActivePowerUpName'] = self.name
        self.PowerUpInfo.text = self.name


    def deactivate(self):
        self.player['PWActive'] = False
        self.PowerUpInfo.text = ""
