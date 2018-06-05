from Objects.Powerups import PartyMode
from Objects.Powerups import ExtraHull
from Objects.Powerups import Speedboost
from Objects.Powerups import SelectedPowerUp
from bge import logic
import random

PartyModeTTL = logic.globalDict['PartyModeTTL']
ExtraHullTTL = logic.globalDict['ExtraHullTTL']
SpeedBoostTTL = logic.globalDict['SpeedBoostTTL']

PartyModeTTL = int(PartyModeTTL)
ExtraHullTTL = int(ExtraHullTTL)
SpeedBoostTTL = int(SpeedBoostTTL)

PartyMode = PartyMode.PartyMode("PartyMode", PartyModeTTL)
ExtraHull = ExtraHull.ExtraHull("ExtraHull", ExtraHullTTL)
Speedboost = Speedboost.Speedboost("SpeedBoost", SpeedBoostTTL)

player = logic.globalDict['local_user']

""""To be able to define the change on getting a powerup, we use a weighted list.
In here you can set the percentages for the powerup"""

# TODO : Maak van de percentage waardes waardes uit de Config

powerUpList = [ExtraHull] * logic.globalDict["ExtraHullChance"] + [Speedboost] * logic.globalDict["SpeedBoostChance"]


def selector():
    """"Here we get te powerup from the list en set it to selectedPowerUp"""
    selectedPowerUp = random.choice(powerUpList)
    logic.globalDict['selectedPowerUp'] = selectedPowerUp
    print("Activate" + str(selectedPowerUp))
    SelectedPowerUp.selected = selectedPowerUp
    selectedPowerUp.activate()


def deactivate():
    cont = logic.getCurrentController()
    own = cont.owner
    if own.sensors['barCheck'].positive:
        try:
            selectedPowerUp = SelectedPowerUp.selected
            print("Deactivate" + str(selectedPowerUp))
            selectedPowerUp.deactivate()
        except AttributeError:
            pass

def OverideDeactivate():
    selectedPowerUp = SelectedPowerUp.selected
    print("Deactivate" + str(selectedPowerUp))
    selectedPowerUp.deactivate()
