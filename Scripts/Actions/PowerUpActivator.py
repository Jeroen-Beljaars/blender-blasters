from bge import logic
from Actions import PowerUpSelector

def activator():
    cont = logic.getCurrentController()
    own = cont.owner
    player = logic.globalDict['local_user']
    pwactive = player['PWActive']
    ob = own.sensors['COL'].hitObject
    print("PWACTIVE = " + str(pwactive))
    if ob is player:
        if pwactive is True:
            print("Overide Deactivate")
            PowerUpSelector.OverideDeactivate()
        PowerUpSelector.selector()
        print("Succes")

    own.endObject()
