import keyboard
from PyQt5.QtCore import QThread, pyqtSignal


class WindowsKeyListener(QThread):
    pressed_shortcut = pyqtSignal(str)
    shortcuts = None

    def __init__(self, shortcuts):
        super().__init__()
        self.shortcuts = shortcuts
        self.add_hotkeys(self.shortcuts)

    def run(self):
        keyboard.wait()

    def add_hotkeys(self, shortcuts):
        for shortcut in shortcuts:
            keyboard.add_hotkey(shortcut,
                                lambda parameter=shortcut:
                                self.pressed_shortcut.emit(parameter))
