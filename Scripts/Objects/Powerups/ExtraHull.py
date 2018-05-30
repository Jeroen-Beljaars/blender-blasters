from Objects.Powerup import PowerUp


class ExtraHull(PowerUp):

    def __init__(self, name, TTL):
        super().__init__(name, TTL)
        self.Hitpoints = 100

    def activate(self):
        super().activate()
        self.player['Hitpoints'] = self.player['Hitpoints'] + self.Hitpoints
        self.setTTL()

    def deactivate(self):
        super().deactivate()
        self.player['Hitpoints'] = self.player['Hitpoints'] - self.Hitpoints
