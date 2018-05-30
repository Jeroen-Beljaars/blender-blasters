from bge import logic
from Actions import PowerUpSelector

def activator():
    cont = logic.getCurrentController()
    own = cont.owner
    player = logic.globalDict['local_user']
    pwactive = player['PWActive']
    ob = own.sensors['COL'].hitObject
    if ob is player:
        if pwactive is True:
            PowerUpSelector.deactivate()
        PowerUpSelector.selector()
        print("Succes")

    own.endObject()
