import sys
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtWidgets import QDialog, QCheckBox, QListWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from UnixKeyListener import MyKeyboardListener
from WindowsKeyListener import WindowsKeyListener


KEY_MODIFIERS = ('CTRL', 'SHIFT', 'ALT')
ORGANIZATION_NAME = 'Martyuk'
ORGANIZATION_DOMAIN = 'martyuk.com'
APPLICATION_NAME = 'KeyListener'


class ShortcutViewer(QDialog):

    def __init__(self, parent=None):
        super(ShortcutViewer, self).__init__(parent)
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


class Main(QMainWindow):
    def __init__(self, parent=None):
        global shortcuts, checkbox_state
        super(Main, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.checkbox = QCheckBox()
        self.shortcut_list = QListWidget()
        self.line_edit = QLineEdit()
        settings = QSettings()
        shortcuts = settings.value('shortcuts', list(), type=list)
        checkbox_state = settings.value('checkbox', True, type=bool)
        self.setup_ui()
        self.shortcut_viewer = ShortcutViewer(self)

    def setup_ui(self):
        widget = QWidget()
        self.shortcut_list.addItems(shortcuts)
        enter_button = QPushButton('enter')
        enter_button.clicked.connect(lambda:
                                     self.add_shortcut(
                                     self.line_edit.text().upper()))
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.line_edit)
        input_layout.addWidget(enter_button)
        modifiers_layout = QHBoxLayout()
        for hint in KEY_MODIFIERS:
            button = QPushButton(self)
            button.setText(hint)
            button_title = button.text()
            button.clicked.connect(lambda ch, text=button_title:
                                   self.add_modifier_to_line_edit(text))
            modifiers_layout.addWidget(button)
        self.checkbox.setText('View')
        self.checkbox.setChecked(checkbox_state)
        self.checkbox.stateChanged.connect(self.change_checkbox_state)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.shortcut_list)
        self.layout.addLayout(input_layout)
        self.layout.addLayout(modifiers_layout)
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.setGeometry(200, 200, 200, 200)
        self.show()

    def add_modifier_to_line_edit(self, modifier):
        current_text = self.line_edit.text()
        self.line_edit.setText(current_text + modifier)

    def add_shortcut(self, shortcut):
        if shortcut not in shortcuts:
            shortcuts.append(shortcut)
            qsettings = QSettings()
            qsettings.setValue('shortcuts', shortcuts)
            qsettings.sync()
            self.shortcut_list.addItem(shortcut)
            self.line_edit.clear()
            if sys.platform == 'win32':
                self.shortcut_viewer.keylistener_thread.add_hotkeys([shortcut])

    def change_checkbox_state(self):
        global checkbox_state
        checkbox_state = self.checkbox.isChecked()
        qsettings = QSettings()
        qsettings.setValue('checkbox', checkbox_state)
        qsettings.sync()
        if self.checkbox.isChecked():
            self.shortcut_viewer.show()
        else:
            self.shortcut_viewer.close()


if __name__ == '__main__':
    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    shortcuts = ()
    checkbox_state = True
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
