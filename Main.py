import sys
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtWidgets import QDialog, QCheckBox, QListWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from UnixKeyListener import MyKeyboardListener
from WindowsKeyListener import WindowsKeyListener
import math

KEY_MODIFIERS = ('CTRL', 'SHIFT', 'ALT')
ORGANIZATION_NAME = 'Martyuk'
ORGANIZATION_DOMAIN = 'martyuk.com'
APPLICATION_NAME = 'KeyListener'


class ShortCutViewer(QDialog):

    def __init__(self, parent=None):
        super(ShortCutViewer, self).__init__(parent)
        print('viewer>> ' + str(shortcuts))
        self.setup_ui()

    def setup_ui(self):
        if sys.platform == 'linux':
            self.threadd = MyKeyboardListener(shortcuts)
            self.threadd.shortcut.connect(self.keyboardChecker)
        elif sys.platform == 'win32':
            self.threadd = WindowsKeyListener(shortcuts)
            self.threadd.pressed_shortcut.connect(self.keyboardChecker)
        self.shortcutLabel = QLabel('s')
        self.layout = QHBoxLayout()
        self.threadd.start()
        self.shortcutLabel.setStyleSheet('''QWidget {
        color: black;
        font-weight: bold;
        font-size: 25px;
        }''')
        self.layout.addWidget(self.shortcutLabel)
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.move(0, 0)
        self.show()

    def keyboardChecker(self, st):
        print(st)
        print(checkboxstate)
        if st in shortcuts and checkboxstate:
            self.show()
            self.shortcutLabel.setText(st.upper())
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.start(1000)
            timer.timeout.connect(self.close)


class Main(QMainWindow):
    def __init__(self, parent=None):
        global shortcuts, checkboxstate
        super(Main, self).__init__(parent)
        qsettings = QSettings()
        shortcuts = qsettings.value('shortcuts', list(), type=list)
        checkboxstate = qsettings.value('checkbox', True, type=bool)
        self.setupUi()

    def setupUi(self):
        self.shortcutviewer = ShortCutViewer(self)
        self.listshrtcuts = QListWidget()
        self.lineEdit = QLineEdit()
        widget = QWidget()
        self.listshrtcuts.addItems(shortcuts)
        enterbutton = QPushButton('enter')
        enterbutton.clicked.connect(lambda:
                                    self.addShortcut(self.lineEdit.text()))
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.lineEdit)
        inputLayout.addWidget(enterbutton)
        hintslayout = QHBoxLayout()
        for hint in KEY_MODIFIERS:
            button = QPushButton(self)
            button.setText(hint)
            text = button.text()
            button.clicked.connect(lambda ch, text=text: self.test(text))
            hintslayout.addWidget(button)

        layout = QVBoxLayout()

        self.checkBox = QCheckBox()
        self.checkBox.setText('View')
        self.checkBox.setChecked(True)
        self.checkBox.stateChanged.connect(self.viewer)

        layout.addWidget(self.checkBox)
        layout.addWidget(self.listshrtcuts)
        layout.addLayout(inputLayout)
        layout.addLayout(hintslayout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setGeometry(200, 200, 200, 200)
        self.show()

    def test(self, hint):
        currentText = self.lineEdit.text()
        self.lineEdit.setText(currentText + hint)

    def addShortcut(self, shortcut):
        if shortcut not in shortcuts:
            shortcuts.append(shortcut)
            qsettings = QSettings()
            qsettings.setValue('shortcuts', shortcuts)
            qsettings.sync()
            self.listshrtcuts.addItem(shortcut)
            self.lineEdit.clear()
            if sys.platform == 'win32':
                self.shortcutviewer.threadd.addHotKeys([shortcut])
                print(shortcuts)

    def viewer(self):
        global checkboxstate
        checkboxstate = self.checkBox.isChecked()
        qsettings = QSettings()
        qsettings.setValue('checkbox', checkboxstate)
        qsettings.sync()
        if self.checkBox.isChecked():
            self.shortcutviewer.show()
        else:
            self.shortcutviewer.close()


if __name__ == '__main__':
    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    shortcuts = ()
    checkboxstate = True
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
