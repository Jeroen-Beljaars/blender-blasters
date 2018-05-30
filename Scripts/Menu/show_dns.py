from bge import logic

if 'dns' in logic.globalDict.keys():
    scene = logic.getCurrentScene()
    message = scene.objects['dns']
    message.text = "ID: " + logic.globalDict['dns']
