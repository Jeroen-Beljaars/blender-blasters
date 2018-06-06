import bge
from Objects.Controller import JoyStick

class ControllerMovement(JoyStick.Joystick):

    def movement(self):
        try:
            player = bge.logic.globalDict['local_user']
            players = bge.logic.globalDict['numOfPlayers']
            if self.joystick != None:
                if players >= 2 or bge.logic.globalDict['TestMode']:
                    btns = self.joystick.activeButtons
                    ''''Check the button pressed, and also if there is only one button pressed'''
                    if 0 in btns:
                        player.applyMovement((player["MovementSpeed"], 0, 0), True)
                    if 1 in btns:
                        print("TEST BUTTON1")
                    if 2 in btns:
                        if bge.logic.globalDict["JumpingPowerUp"] is True:
                            bge.types.KX_CharacterWrapper.jump(bge.constraints.getCharacter(player))
                    if 3 in btns:
                        print("TEST BUTTON3")
                    if 4 in btns:
                        print("TEST BUTTON4")
                    if 5 in btns:
                        print("TEST BUTTON5")
                    if 6 in btns:
                        print("TEST BUTTON6")
                    if 7 in btns:
                        print("TEST BUTTON7")
                    if 8 in btns:
                        print("TEST BUTTON8")
                    if 9 in btns:
                        print("TEST BUTTON9")
                    if 10 in btns:
                        print("TEST BUTTON10")
                    if 11 in btns:
                        print("TEST BUTTON11")

                    up = 1
                    down = 4
                    left = 8
                    right = 2
                    upLeft = 9
                    upRight = 3
                    downLeft = 12
                    downRight = 6

                    hats = self.joystick.hatValues
                    if up in hats:
                        print(hats)
                    elif left in hats:
                        print(hats)
                    elif right in hats:
                        print(hats)
                    elif down in hats:
                        print(hats)
                    elif upLeft in hats:
                        print(hats)
                    elif upRight in hats:
                        print(hats)
                    elif downLeft in hats:
                        print(hats)
                    elif downRight in hats:
                        print(hats)

                    av = self.joystick.axisValues
                    left_analog_x = av[0]
                    left_analog_y = av[1]
                    right_analog_x = av[2]
                    right_analog_y = av[3]
                    dead_zone = .50
                    if abs(left_analog_y) > dead_zone:
                        # player.applyRotation((0, 0, 0.05), False)
                        pass
                    if abs(left_analog_x) > dead_zone:
                        player.applyRotation((0, 0, -0.05 * left_analog_x), False)
        except KeyError:
            pass

mv = ControllerMovement()


def movement():
    mv.movement()
