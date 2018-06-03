from bge import logic


cont = logic.getCurrentController()
own = cont.owner
own['Music'] = True

print(own.actuators)


