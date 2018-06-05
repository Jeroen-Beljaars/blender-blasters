from Objects.Powerup import PowerUp


class ExtraHull(PowerUp):

    def __init__(self, name, TTL):
        super().__init__(name, TTL)
        self.Hitpoints = 50

    def activate(self):
        super().activate()
        self.player['Hitpoints'] += self.Hitpoints
        self.setTTL()

    def deactivate(self):
        super().deactivate()
