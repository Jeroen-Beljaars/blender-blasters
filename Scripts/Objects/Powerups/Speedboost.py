from Objects.Powerup import PowerUp
from bge import logic


class Speedboost(PowerUp):

    def __init__(self, name, TTL):
        super().__init__(name, TTL)
        self.speedBoost = 2

    def activate(self):
        super().activate()
        self.player['MovementSpeed'] = self.player['MovementSpeed'] * self.speedBoost
        self.setTTL()

    def deactivate(self):
        super().deactivate()
        self.player['MovementSpeed'] = (logic.globalDict["MovementSpeed"]/1000)

