""""Sets the path for the Python files for Blender to refrance to"""

import os
import sys
t = os.getcwd() + "\Scripts"
if t not in sys.path:
    sys.path.insert(0, t)

print("System Path is : " + t)