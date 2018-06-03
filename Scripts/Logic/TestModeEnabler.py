from bge import logic


class testMode:

    def __init__(self):
        self.cont = logic.getCurrentController()
        self.own = self.cont.owner
        self.testMode = self.own['TestMode']

    def setTestMode(self):
        logic.globalDict['TestMode'] = self.testMode
        print(self.testMode)


ts = testMode()


def setTestMode():
    ts.setTestMode()
