from bge import logic

winner = logic.globalDict['winner']
scene = logic.getCurrentScene()
message = scene.objects['winner']
message.text = "Team {} Won!".format(winner)