import configparser
import os
from bge import logic

""""
In this file we load up the configuration file
Here the values will be checked and set.
If values appear to be False on the input the basic values will be called from this file
"""

""""
Basic game values for refrance of the game. of values on the config file are False these settings will be used
for the False value
"""

if not 'key_binding' in logic.globalDict.keys():
    logic.globalDict['key_binding'] = {'forward': 119, 'back': 115, 'left': 97, 'right': 100, 'shoot': 32,
                                       'powerup': 13}

# powerups
PartyModeTTL = 5
ExtraHullTTL = 15
SpeedBoostTTL = 10
PartyModeChance = 25
ExtraHullChance = 40
SpeedBoostChance = 35

# TankStats
MovementSpeed = 100
Hitpoints = 50
FirePower = 25

# Cheats
JumpingPowerUp = False
PartyModeForEver = False
TurtleMode = False

# safetyNet
safetyNet = True

configParser = configparser.RawConfigParser()
cfp = os.getcwd() + "\Config\TankConfig.txt"
# cfp = "C:/Users\Zilverdrake\Documents\PADBLE10\Config/TankConfig.txt"#this is pure for local testing
print(cfp)
configParser.read(cfp)
print(configParser.sections())

""""
Here we set the restriction values. These are used as a safety net so the players don't break the game.
"""

safetyNetCheck = configParser.getboolean('safetyNet', 'safetyNet', fallback=True)
print(safetyNetCheck)

# set the Min and Max TTL time
TTLRange = range(1, 60)
# set the Max Powerup List Size
maxListSize = 100
# set tank stats
MovementSpeedRange = range(49, 451)
HitPointsRange = range(0, 5001)
FirePowerRange = range(0, 1001)

""""
At this points we make a list for all the values that we need. We fist initialise all the config values.
Then we add those values to a list. We make list for all the things that are needed in the reading and checking
of the config file.
"""

# Init all the config values
partyModeConfig = None
extraHullConfig = None
speedBoostConfig = None
partyModeChanceConfig = None
extraHullChanceConfig = None
speedBoostChanceConfig = None
MovementSpeedConfig = None
HitpointsConfig = None
FirePowerConfig = None
JumpingPowerUpConfig = None
PartyModeForEverConfig = None
TurtleModeConfig = None
# list for the sections of the config file
sections = [
    "Powerups",
    "TankStats",
    "Cheats"
]
# list with the config variables to store the variables in
values = [
    partyModeConfig,
    extraHullConfig,
    speedBoostConfig,
    partyModeChanceConfig,
    extraHullChanceConfig,
    speedBoostChanceConfig,
    MovementSpeedConfig,
    HitpointsConfig,
    FirePowerConfig,
    JumpingPowerUpConfig,
    PartyModeForEverConfig,
    TurtleModeConfig

]
# list to store the fallback values in
fallBack = [
    PartyModeTTL,
    ExtraHullTTL,
    SpeedBoostTTL,
    PartyModeChance,
    ExtraHullChance,
    SpeedBoostChance,
    MovementSpeed,
    Hitpoints,
    FirePower,
    JumpingPowerUp,
    PartyModeForEver,
    TurtleMode
]
# a list for all the config values
config = [
    "PartyModeTTL",
    "ExtraHullTTL",
    "SpeedBoostTTL",
    "PartyModeChance",
    "ExtraHullChance",
    "SpeedBoostChance",
    "MovementSpeed",
    "HitPoints",
    "FirePower",
    "JumpingPowerUp",
    "PartyModeForEver",
    "TurtleMode"

]
# list for the tank ranges
TankStatRange = [
    MovementSpeedRange,
    HitPointsRange,
    FirePowerRange

]

ValueList = []  # this list will be filled with the check values
section = 0  # This is a variable for indication the section that needs to be read from
tsr = 0  # This is a variable to indicate the ranges list that needs to be read
count = 0  # this variable if for summing the total chance amount
for i, y in enumerate(values):
    print(config[i])
    ''''At the start of the loop the try clause will be opend'''
    try:
        if i < 9:  # The fist 8 values are all int. So we can use the getint
            values[i] = configParser.getint(sections[section], config[i], fallback=fallBack[i])
            if i < 3:  # the first 3 values are for the TTL
                if values[i] in TTLRange:
                    ValueList.append(values[i])
                else:
                    ValueList.append(fallBack[i])
            elif i >= 3 and i <= 5:  # The 4,5,6 value are for the powerup chance
                print("ADDING")
                count += values[i]  # adds al the chance values together
                if i == 5:  # When the index is 5 all chance values have been added and will be checkt if they are 100 together
                    print(count)
                    if count != maxListSize:
                        print("Ongeldige Waarden. Zet waarde op DEF")
                        ValueList.append(fallBack[3])
                        ValueList.append(fallBack[4])
                        ValueList.append(fallBack[5])
                    else:
                        ValueList.append(values[3])
                        ValueList.append(values[4])
                        ValueList.append(values[5])

            elif i >= 6 and i <= 8:  # this section checks the TankStats
                if values[i] in TankStatRange[tsr]:
                    ValueList.append(values[i])
                    tsr += 1
                else:
                    ValueList.append(fallBack[i])
                    tsr += 1
            if i == 5:  # this section sets the section that has to be loaded from the file
                section += 1
                print(sections[section])

            if i == 8:  # this section sets the section that has to be loaded from the file
                section += 1
                print(sections[section])
        elif i >= 9 and i <= 11:  # here we use the get bool for the boolean values of the config file
            values[i] = configParser.getboolean(sections[section], config[i], fallback=fallBack[i])
            ValueList.append(values[i])

    except Exception as e:  # in case there is a mayor error in the config file, the default value will be set.
        print(e)
        values[i] = fallBack[i]
        ValueList.append(values[i])

print(ValueList)  # check for the console to read uit the values
# When all the items are correct they will be added to the dictionary for other files to use
configlist = []
for i, y in enumerate(ValueList):
    configlist.append(ValueList[i])
    logic.globalDict[config[i]] = ValueList[i]
print(configlist)
logic.globalDict["configlist"] = configlist