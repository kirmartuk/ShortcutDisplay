from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard

key_pressed = ['', '', '']


class MyKeyboardListener(QThread):
    pressed_shortcut = pyqtSignal(str)
    shortcuts = None

    def __init__(self, shortcuts):
        self.shortcuts = shortcuts
        super().__init__()

    def run(self):
        def on_press(key):
            try:
                key_pressed.append(key.char)
                key_pressed.pop(0)
            except AttributeError:
                key_pressed.append(str(key)[4:])
                key_pressed.pop(0)
            finally:
                if key_pressed[0] is not None and \
                        key_pressed[1] is not None and \
                        key_pressed[2] is not None:
                    if str(
                            key_pressed[1].upper()
                            + '+'
                            + key_pressed[2].upper()
                    ) in self.shortcuts:
                        self.pressed_shortcut.emit(str(
                            key_pressed[1]
                            + '+'
                            + key_pressed[2]
                        ).upper())
                    if str(
                            key_pressed[0].upper()
                            + '+'
                            + key_pressed[1].upper()
                            + '+'
                            + key_pressed[2].upper()
                    ) in self.shortcuts:
                        self.pressed_shortcut.emit(str(
                            key_pressed[0].upper()
                            + '+'
                            + key_pressed[1].upper()
                            + '+'
                            + key_pressed[2].upper()
                        ))

        # Collect events until released
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=on_press)
        listener.start()
