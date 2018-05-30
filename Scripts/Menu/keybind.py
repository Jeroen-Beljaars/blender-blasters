from bge import logic, events


class KeyBind:
    def __init__(self):
        self.key_map = {13: 'ENTER', 32: 'SPACE', 42: 'PADASTER', 44: 'COMMA', 45: 'MINUS', 46: 'PERIOD', 48: 'ZERO',
                        49: 'ONE',
                        50: 'TWO', 51: 'THREE', 52: 'FOUR', 53: 'FIVE', 54: 'SIX', 55: 'SEVEN', 56: 'EIGHT', 57: 'NINE',
                        97: 'A',
                        98: 'B', 99: 'C', 100: 'D', 101: 'E', 102: 'F', 103: 'G', 104: 'H', 105: 'I', 106: 'J',
                        107: 'K',
                        108: 'L',
                        109: 'M', 110: 'N', 111: 'O', 112: 'P', 113: 'Q', 114: 'R', 115: 'S', 116: 'T', 117: 'U',
                        118: 'V',
                        119: 'W', 120: 'X', 121: 'Y', 122: 'Z', 124: 'LEFTCTRL', 125: 'LEFTALT', 126: 'RIGHTALT',
                        127: 'RIGHTCTRL',
                        128: 'RIGHTSHIFT', 129: 'LEFTSHIFT', 130: 'ESC', 131: 'TAB', 132: 'LINEFEED', 133: 'BACKSPACE',
                        134: 'DEL',
                        135: 'SEMICOLON', 136: 'QUOTE', 137: 'ACCENTGRAVE', 138: 'SLASH', 139: 'BACKSLASH',
                        140: 'EQUAL',
                        141: 'LEFTBRACKET', 142: 'RIGHTBRACKET', 143: 'LEFTARROW', 144: 'DOWNARROW', 145: 'RIGHTARROW',
                        146: 'UPARROW', 147: 'PAD2', 148: 'PAD4', 149: 'PAD6', 150: 'PAD8', 151: 'PAD1', 152: 'PAD3',
                        153: 'PAD5',
                        154: 'PAD7', 155: 'PAD9', 156: 'PADPERIOD', 157: 'PADSLASH', 158: 'PAD0', 159: 'PADMI',
                        160: 'PADEN',
                        161: 'PADPLUS', 162: 'F1', 163: 'F2', 164: 'F3', 165: 'F4', 166: 'F5', 167: 'F6', 168: 'F7',
                        169: 'F8',
                        170: 'F9', 171: 'F10', 174: 'PAUSE', 175: 'INSERT', 176: 'HOME', 177: 'PAGEUP', 178: 'PAGEDOWN',
                        182: 'F11',
                        183: 'F12', 186: 'END'}

        self.bind_properties = {
            'forward': {
                'active': False,
                'value': 119,
                'field': None
            },
            'back': {
                'active': False,
                'value': 115,
                'field': None
            },
            'left': {
                'active': False,
                'value': 97,
                'field': None
            },
            'right': {
                'active': False,
                'value': 100,
                'field': None
            },
            'shoot': {
                'active': False,
                'value': 32,
                'field': None
            },
            'powerup': {
                'active': False,
                'value': 13,
                'field': None
            }
        }

        self.message = None

    def detect(self):
        cont = logic.getCurrentController()
        own = cont.owner

        for key in self.bind_properties.keys():
            if self.bind_properties[key]['active']:
                for event in own.sensors['Keyboard'].events:
                    if event[1] == 1:
                        if not event[0] in [x['value'] for x in self.bind_properties.values()]:
                            try:
                                self.bind_properties[key]['field'].text = self.key_map[event[0]]
                                self.bind_properties[key]['value'] = event[0]
                            except KeyError:
                                pass
                        else:
                            self.message.text = "That key is allready being used!"
                            self.message.color = [1, 0, 0, 1]

    def save(self):
        logic.globalDict['key_binding'] = {
            key: value['value'] for (key, value) in self.bind_properties.items()
        }
        self.message.text = "Keybindings saved succesfully!"
        self.message.color = [0, 1, 0, 1]

    def load_default(self):
        scene = logic.getCurrentScene()
        for key, value in self.bind_properties.items():
            value['field'] = scene.objects[key]
        self.message = scene.objects['bind_message']

        if 'key_bind' in logic.globalDict.keys():
            for key, value in logic.globalDict.items():
                self.bind_properties[key]['value'] = value

        for value in self.bind_properties.values():
            value['field'].text = self.key_map[value['value']]


keybind = KeyBind()


def load_default():
    keybind.load_default()


def detect():
    keybind.detect()


def save():
    keybind.save()


def forward():
    deactivate()
    keybind.bind_properties['forward']['active'] = True


def back():
    deactivate()
    keybind.bind_properties['back']['active'] = True


def left():
    deactivate()
    keybind.bind_properties['left']['active'] = True


def right():
    deactivate()
    keybind.bind_properties['right']['active'] = True


def shoot():
    deactivate()
    keybind.bind_properties['shoot']['active'] = True


def powerup():
    deactivate()
    keybind.bind_properties['powerup']['active'] = True


def deactivate():
    for key in keybind.bind_properties.keys():
        keybind.bind_properties[key]['active'] = False
