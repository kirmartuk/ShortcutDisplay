import sys

from PyQt5.QtCore import QSettings, QTimer, Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel

from UnixKeyListener import MyKeyboardListener
from WindowsKeyListener import WindowsKeyListener

shortcuts = None
checkbox_state = None


class ShortcutDisplay(QDialog):

    def __init__(self, parent=None):
        global shortcuts, checkbox_state
        super(ShortcutDisplay, self).__init__(parent)
        settings = QSettings()
        shortcuts = settings.value('shortcuts', list(), type=list)
        checkbox_state = settings.value('checkbox', True, type=bool)
        self.layout = QHBoxLayout()
        self.shortcut_label = QLabel()
        if sys.platform == 'linux':
            self.keylistener_thread = MyKeyboardListener(shortcuts)
            self.keylistener_thread.pressed_shortcut\
                .connect(self.show_shortcut)
        elif sys.platform == 'win32':
            self.keylistener_thread = WindowsKeyListener(shortcuts)
            self.keylistener_thread.pressed_shortcut\
                .connect(self.show_shortcut)
        self.setup_ui()

    def setup_ui(self):
        self.keylistener_thread.start()
        self.shortcut_label.setStyleSheet('''QWidget {
        color: #47f9ff;
        font-weight: bold;
        font-size: 25px;
        }''')
        self.layout.addWidget(self.shortcut_label)
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.move(0, 0)
        self.show()

    def show_shortcut(self, shortcut):
        if shortcut in shortcuts and checkbox_state:
            self.show()
            self.shortcut_label.setText(shortcut.upper())
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.start(1000)
            timer.timeout.connect(self.close)
