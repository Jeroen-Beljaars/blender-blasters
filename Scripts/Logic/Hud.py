from bge import logic



def update():
    try:
        scene = logic.getSceneList()[0]


        Tower1 = scene.objects['TowerTeam1']
        Tower2 = scene.objects['TowerTeam2']

        player = logic.globalDict['local_user']
        hud = logic.getSceneList()[-1]
        TankHP = hud.objects['TankHP']
        TankHP.text = str(player['Hitpoints'])
        TowerTeamOneHP = hud.objects['Tower1HP']
        TowerTeamTwoHP = hud.objects['Tower2HP']
        TowerTeamOneHP.text = str(Tower1['Tower_Health'])
        TowerTeamTwoHP.text = str(Tower2['Tower_Health'])
    except:
        pass


