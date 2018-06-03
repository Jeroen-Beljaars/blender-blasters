from bge import logic
from random import randint


def spawn():
    cont = logic.getCurrentController()
    own = cont.owner
    scene = logic.getCurrentScene()
    col = own.sensors['Reset']
    players = logic.globalDict['numOfPlayers']

    if own['Spawn'] is False and players >= 2:
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
