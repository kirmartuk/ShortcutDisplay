from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard


class MyKeyboardListener(QThread):
    shortcut = pyqtSignal(str)
    shortcuts = None

    def __init__(self, shortcuts):
        self.shortcuts = shortcuts
        super().__init__()

    def run(self):
        def on_press(key):
            try:
                self.shortcut.emit(key.char)
            except AttributeError:
                self.shortcut.emit(str(key)[4:])
            finally:
                pass

        # Collect events until released
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=on_press)
        listener.start()
