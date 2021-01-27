from Checker.CropingPhotos import *
from Checker.Handler import *
import time


class CommandPicker:
    def __init__(self):
        time.sleep(4)
        self.CropObj = Croper()
        self.HandlerObj = Handler()


Checker = CommandPicker()
