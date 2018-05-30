import bge
import client


def detector():
    cont = bge.logic.getCurrentController()
    own = cont.owner
    bls = own.sensors['Bullet']
    if bls.positive:
        if bls.hitObject['team'] != own['team']:
            if own['Hitpoints'] <= 0:
                client.respawn()
            else:
                own['Hitpoints'] -= own['Power']
