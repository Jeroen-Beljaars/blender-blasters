from bge import logic, events
import bge


def keyDown(key_code=events.WKEY, status=logic.KX_INPUT_ACTIVE):
    """
    This method checks if the key (key_code) is active
    i.e. keyDown(events.WKEY) checks if the w_key is being pressed
    """
    if logic.keyboard.events[key_code] == status:
        return True
    return False


class Movement():

    def PlayerMovement(self):
        try:
            cont = logic.getCurrentController()
            own = cont.owner
            try:
                player = logic.globalDict['local_user']
                forwardMovement = player['MovementSpeed']
            except:
                pass
            else:
                # Basic movement (forward, backwards, left, right)
                key_bindings = logic.globalDict['key_binding']
                forward = keyDown(key_bindings['forward'])
                backward = keyDown(key_bindings['back'])
                left = keyDown(key_bindings['left'])
                right = keyDown(key_bindings['right'])
                powerup = keyDown(key_bindings['powerup'])

                if forward:
                    player.applyMovement((forwardMovement, 0, 0), True)

                elif backward:
                    player.applyMovement((-forwardMovement, 0, 0), True)

                if left:
                    player.applyRotation((0, 0, 0.05), False)
                elif right:
                    player.applyRotation((0, 0, -0.05), False)
                if powerup and logic.globalDict['JumpingPowerUp'] is True:
                    print("ENTER KEY")
                    bge.types.KX_CharacterWrapper.jump(bge.constraints.getCharacter(player))
        except:
            print("No active player found")



movement = Movement()

def move():
    movement.PlayerMovement()
