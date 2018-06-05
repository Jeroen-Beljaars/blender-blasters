from bge import logic
from Logic import Hud


# File for the distructable tower object

class Tower:
    def hit(self):
        scene = logic.getCurrentScene()
        tank = scene.objects['Tank']
        tower1 = scene.objects['TowerTeam1']
        tower2 = scene.objects['TowerTeam2']
        cont = logic.getCurrentController()
        own = cont.owner
        sensor = cont.sensors['Collision']
        hud = logic.getSceneList()[-1]

        if sensor.positive:
            own['Tower_Health'] = own['Tower_Health'] - tank['Power']
            if own is tower1:
                Hud.updateTOneBar()
            if own is tower2:
                Hud.updateTTwoBar()
            if own['Tower_Health'] <= 0:
                team = own['team']
                if team == "team2":
                    hud = logic.getSceneList()[-1]
                    hud.objects['team1_score'].text = str(int(hud.objects['team1_score'].text) + 1)
                else:
                    hud.objects['team2_score'].text = str(int(hud.objects['team2_score'].text) + 1)

                team1_counter = 1
                team2_counter = 3
                for object in scene.objects:
                    if object.name == "Tank":
                        team = object['team']
                        object['Hitpoints'] = logic.globalDict['HitPoints']
                        if team == "team1":
                            spawner = scene.objects['Spawner{}'.format(team1_counter)]
                            object.worldPosition = spawner.worldPosition
                            if team1_counter == 2:
                                object.localOrientation = [0, 0, -3]
                                team1_counter = 1
                            else:
                                object.localOrientation = [0,0,0.1]
                                team1_counter += 1
                        else:
                            spawner = scene.objects['Spawner{}'.format(team2_counter)]
                            object.worldPosition = spawner.worldPosition
                            if team2_counter == 4:
                                object.localOrientation =[0, 0, 0.1]
                                team2_counter = 3
                            else:
                                object.localOrientation = [0, 0, -3]
                                team2_counter += 1
                tower1['Tower_Health'] = 250
                tower2['Tower_Health'] = 250
                Hud.reset_bars()
                Hud.updateTOneBar()
                Hud.updateTTwoBar()
                logic.globalDict['current_match'] += 1
                print("-----------------------------------------------------------")
                print(logic.globalDict['current_match'])
                print(logic.globalDict['matches'])
                print("-----------------------------------------------------------")
                if logic.globalDict['current_match'] >= logic.globalDict['matches']:
                    if int(hud.objects['team2_score'].text) > int(hud.objects['team1_score'].text):
                        logic.globalDict['winner'] = "2"
                    else:
                        logic.globalDict['winner'] = "1"
                    for scene in logic.getSceneList():
                        if scene.name == 'Game':
                            scene.replace('won')
                    own.endObject()


tower = Tower()


def hit():
    tower.hit()


def collision():
    cont = logic.getCurrentController()
    own = cont.owner
    sensor = cont.sensors['Collision']
    if sensor.positive:
        bullet = sensor.hitObject
        bullet_team = bullet['team']
        tower_team = own['team']

        if bullet_team != tower_team:
            tower.hit()
