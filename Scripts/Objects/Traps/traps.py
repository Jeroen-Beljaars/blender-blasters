from bge import logic
import time
from threading import Thread

class Traps():
    def __init__(self, seconds = 10):
        self.player = logic.globalDict['local_user']
        self.forwardMovement = self.player['MovementSpeed']
        self.seconds = seconds

    def collide(self):
        controller = logic.getCurrentController()
        own = controller.owner
        sensor = own.sensors['Collision']
        if sensor.positive:
            print("trap triggered")
            sensor.hitObject['MovementSpeed'] = 0
            timer = Thread(target=self.timer, args=(own, 6))
            timer.start()

    def timer(self, own, seconds):
        time.sleep(seconds)
        self.player['MovementSpeed'] = 0.1

trap = Traps()

def collide():
    trap.collide()


