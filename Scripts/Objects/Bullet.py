import bge
import os


# File for the Bullet object shot by the tanks

class Bullet:

    def hit(self):
        cont = bge.logic.getCurrentController()
        own = cont.owner
        print("Object Hit")
        #own.endObject()

    def movement(self):

        cont = bge.logic.getCurrentController()
        own = cont.owner
        own.applyForce((2000, 0, 0), True)


bullet = Bullet()


def hit():
    bullet.hit()


def movement():
    bullet.movement()
