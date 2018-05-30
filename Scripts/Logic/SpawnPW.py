from bge import logic
from random import randint


def spawn():
    cont = logic.getCurrentController()
    own = cont.owner
    scene = logic.getCurrentScene()
    col = own.sensors['Reset']

    if own['Spawn'] is False:
        try:
            rng = logic.globalDict['RandomNumber']
            if rng == own['RN']:
                scene.addObject("Powerup", own)
                own['Spawn'] = True
                print(own['Spawn'])
        except KeyError:
            pass

def reset():
    cont = logic.getCurrentController()
    own = cont.owner
    scene = logic.getCurrentScene()
    col = own.sensors['Reset']
    if col.positive and own['Spawn'] is True:
        own['Spawn'] = False
