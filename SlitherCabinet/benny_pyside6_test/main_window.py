# Operating system
""" none """
# Python packages
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QFile, QSize, QEvent
from PySide6.QtGui import Qt, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QToolButton, QStyle
# Local modules
""" none """


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initial_pos = None
        self.normal_window_state = None

    # Load main_window.ui
        qfile = QFile("main_window.ui")
        qfile.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(qfile)
        qfile.close()

    # Set Window Flags
        # Hide OS default Titlebar
        self.window.setWindowFlags(self.window.windowFlags() | Qt.FramelessWindowHint)
        # For OS taskbar
        self.window.setWindowIcon(QIcon("window.png"))
        # Keyboard input focus
        #self.window.setFocusPolicy(Qt.StrongFocus)
        # Enable mouse tracking
        self.window.setMouseTracking(True)
        # installEventFilter
        self.window.installEventFilter(self)

    # Initialise, connect and set icon for tool buttons
        # Combined Title / Menu Bar (custom)
        # Menu button
        self.toolButton_menu = self.window.findChild(QToolButton, "toolButton_menu")
        self.toolButton_menu.setIcon(QIcon("menu.png"))
        self.toolButton_menu.clicked.connect(self.menu_function)

        # Minimize button
        self.toolButton_minimize = self.window.findChild(QToolButton, "toolButton_minimize")
        minimize_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)
        self.toolButton_minimize.setIcon(QIcon(minimize_icon))
        self.toolButton_minimize.clicked.connect(self.minimize_function)

        # Normal button
        self.toolButton_normal = self.window.findChild(QToolButton, "toolButton_normal")
        normal_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton)
        self.toolButton_normal.setIcon(QIcon(normal_icon))
        self.toolButton_normal.clicked.connect(self.normal_function)
        self.toolButton_normal.setVisible(False)

        # Maximize button
        self.toolButton_maximize = self.window.findChild(QToolButton, "toolButton_maximize")
        maximum_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton)
        self.toolButton_maximize.setIcon(QIcon(maximum_icon))
        self.toolButton_maximize.clicked.connect(self.maximize_function)

        # Close button
        self.toolButton_close = self.window.findChild(QToolButton, "toolButton_close")
        close_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)
        self.toolButton_close.setIcon(QIcon(close_icon))
        self.toolButton_close.clicked.connect(self.close_function)

    # Combined Title / Menu Bar Functions (custom)
    def menu_function(self):
        pass

    def minimize_function(self):
        self.window.showMinimized()

    def normal_function(self):
        self.window.setWindowState(self.normal_window_state)
        self.toolButton_normal.setVisible(False)
        self.toolButton_maximize.setVisible(True)

    def maximize_function(self):
        self.normal_window_state = self.window.windowState()
        self.window.showMaximized()
        self.toolButton_maximize.setVisible(False)
        self.toolButton_normal.setVisible(True)

    def close_function(self):
        self.window.close()


    # Event Filter
    '''def eventFilter(self, source, event):
        # left button double click
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
                print("event")

        return super(MainWindow, self).eventFilter(source, event)'''

    '''def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            print("QtCore.QEvent.MouseButtonPress")
            if event.button() == QtCore.Qt.LeftButton:
                print("event")
                self.window.move(event.globalX(), event.globalY())

        return super(MainWindow, self).eventFilter(source, event)'''