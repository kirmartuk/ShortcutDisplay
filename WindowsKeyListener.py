import keyboard
from PyQt5.QtCore import QThread, pyqtSignal


class WindowsKeyListener(QThread):
    pressed_shortcut = pyqtSignal(str)
    shortcuts = None

    def __init__(self, shortcuts):
        super().__init__()
        self.shortcuts = shortcuts
        self.addHotKeys(self.shortcuts)

    def run(self):
        keyboard.wait()

    def addHotKeys(self, shortcuts):
        print('sst')
        for shortcut in shortcuts:
            keyboard.add_hotkey(shortcut, lambda parameter=shortcut: self.pressed_shortcut.emit(parameter))
