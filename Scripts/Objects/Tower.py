from bge import logic
import os

#File for the distructable tower object

class Tower:
    def hit(self):
        scene = logic.getCurrentScene()
        tank = scene.objects['Tank']
        cont = logic.getCurrentController()
        own = cont.owner
        sensor = cont.sensors['Collision']
        if sensor.positive:
            own['Tower_Health'] = own['Tower_Health'] - tank['Power']
            print("TOWER HIT")
            print(own['Tower_Health'])
            print(own.sensors['Collision'].hitObject)
            if own['Tower_Health'] <= 0:
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