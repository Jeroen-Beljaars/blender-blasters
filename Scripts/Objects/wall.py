import bge
import os


# File for the distructable wall object

class wall:

    def hit(self):

        tank = int(bge.logic.globalDict['FirePower'])

        cont = bge.logic.getCurrentController()
        own = cont.owner
        if own.sensors['Hit'].positive:
            own['Wall_Health'] = own['Wall_Health'] - tank
            print("HIT")
        if own['Wall_Health'] <= 0:
            own.endObject()




wall = wall()


def hit():
    wall.hit()
