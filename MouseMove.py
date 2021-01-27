from pyautogui import moveTo, scroll

one_block_size = 72  # 72 normal


class MouseMover:
    def __init__(self):
        pass

    def start_move_down(self):
        moveTo(1900, 392)
        scroll(-75)

    def block_move_down(self):
        scroll(-86)
