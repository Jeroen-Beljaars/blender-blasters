import bge

cont = bge.logic.getCurrentController()
own = cont.owner
player = bge.logic.globalDict['local_user']
own.setParent(player)



