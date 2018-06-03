from bge import logic


class PowerUp:

    def __init__(self, name, TTL):
        self.player = logic.globalDict['local_user']
        self.name = name
        self.TTL = TTL
        self.hud = logic.getSceneList()[-1]
        self.PowerUpInfo = self.hud.objects['PowerUpName']
        self.PowerUpBar = self.hud.objects['PowerUpBar']
        self.PowerUpLogic = self.PowerUpBar.actuators['lifeTTL']

    def setTTL(self):
        self.player['Timer'] = self.TTL
        self.PowerUpBar['lifeTTL'] = float(0)
        self.PowerUpBar['Timer'] = float(self.TTL)
        self.PowerUpLogic.value = str((100 / self.TTL) / 60)
        print(self.TTL)

    def activate(self):
        self.player['PWActive'] = True
        self.player['ActivePowerUpName'] = self.name
        self.PowerUpInfo.text = self.name

    def deactivate(self):
        self.player['PWActive'] = False
        self.PowerUpInfo.text = ""
