"""
This is the c class file for the power up PartyMode
It makes the tank shoot shoot faster for 5 times 60 frames
It also sets the power of the tank to the power of the power up
On the ending of the power up the power of the tank will be reset to the base value
"""
from Objects.Powerup import PowerUp
from bge import logic


class PartyMode(PowerUp):

    def __init__(self, name, TTL):
        super().__init__(name, TTL)
        self.power = 5

    def activate(self):
        super().activate()
        self.player['Power'] = self.power
        self.player['PartyMode'] = True
        self.setTTL()

    def deactivate(self):
        super().deactivate()
        self.player['Power'] = logic.globalDict['FirePower']
        print("Deactivate partymode")
        self.player['PartyMode'] = False

