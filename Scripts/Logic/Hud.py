from bge import logic
def update():
    try:
        hud = logic.getSceneList()[-1]
        gameScene = logic.getSceneList()[0]
        Tower1 = gameScene.objects['TowerTeam1']
        Tower2 = gameScene.objects['TowerTeam2']
        player = logic.globalDict['local_user']

        TankHP = hud.objects['TankHP']
        TankHP.text = str(player['Hitpoints'])
        TowerTeamOneHP = hud.objects['Tower1HP']
        TowerTeamTwoHP = hud.objects['Tower2HP']
        TowerTeamOneHP.text = str(Tower1['Tower_Health'])
        TowerTeamTwoHP.text = str(Tower2['Tower_Health'])
    except:
        pass

def updateTOneBar():
    hud = logic.getSceneList()[-1]
    t1bar = hud.objects['Tower1HPBar']
    t1bar["lifeT1"] = t1bar["lifeT1"] + 10


def updateTTwoBar():
    hud = logic.getSceneList()[-1]
    t2bar = hud.objects['Tower2HPBar']
    t2bar["lifeT2"] = t2bar["lifeT2"] + 10

def reset_bars():
    hud = logic.getSceneList()[-1]
    hud.objects['Tower1HPBar']['lifeT1'] = 0
    hud.objects['Tower2HPBar']['lifeT2'] = 0
