# Operating system
"""None"""
# Python packages
"""import module_name:
   This statement imports the entire module. To access items from the module, 
   you need to use the module name as a prefix (e.g., module_name.item_name)."""
import math
import pygame
"""from module_name import item_name:
   This statement imports specific items directly into the current namespace. 
   You can then access these items without the module name prefix (e.g., item_name)."""
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QApplication
# Local modules
"""None"""

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        """Class variables"""
        self.CONST_ISO = math.degrees(math.asin(math.sqrt(2 / 3)))  # ~54.73 degrees
        self.doubleclick = None
        self.mouse_y = None
        self.mouse_x = None
        self.real_time_mouse_x = None
        self.real_time_mouse_y = None
        # Mouse drag event
        self.first = True
        self.pitch = None
        self.previous = pygame.Vector2(0, 0)
        self.sensitivity = 2
        self.roll = None
        self.yaw = None
        self.zoom = None
        # Button state
        self.toolButton_clicked = 0
        self.toolButton_dimetric_clicked = 0
        self.toolButton_isometric_clicked = 0
        self.toolButton_previous = ""
        self.view = '3D'
        self.yaw2D = 0

        """Load XML user interface from (QtDesigner) as .ui"""
        uic.loadUi('ui/MainWindow.ui', self)

        """Initialize Tool Buttons"""
        self.toolButton_2D.clicked.connect(self.two_d_function)
        self.toolButton_3D.clicked.connect(self.three_d_function)
        self.toolButton_trimetric.clicked.connect(self.trimetric_function)
        self.toolButton_dimetric.clicked.connect(self.dimetric_function)
        self.toolButton_isometric.clicked.connect(self.isometric_function)

    """Class functions"""
    def setup_ui(self):
        pass

    # openGL specific
    def initialise_gl(self):
        pass

    def camera_init(self):
        pass

    def render_gl(self):
        pass

    # x(roll) y(pitch) z(yaw)) rotations -> Z up environment
    def two_d_function(self):
        # set view
        self.view = '2D'
        # clear other buttons states
        self.toolButton_trimetric.setChecked(False)
        self.toolButton_dimetric.setChecked(False)
        self.toolButton_dimetric.setIcon(QIcon('icons/mode-3d-dimetric-wireframe.png'))
        self.toolButton_isometric.setChecked(False)
        self.toolButton_isometric.setIcon(QIcon('icons/mode-3d-isometric-wireframe.png'))
        # set to 3D mode
        self.toolButton_2D.setChecked(True)
        self.toolButton_3D.setChecked(False)
        # set corresponding axis rotations
        self.toolButton_Xroll.setChecked(False)
        self.toolButton_Ypitch.setChecked(False)
        self.toolButton_Zyaw.setChecked(True)
        # hide non corresponding
        self.toolButton_Xroll.setEnabled(False)
        self.toolButton_Ypitch.setEnabled(False)
        self.toolButton_Zyaw.setEnabled(True)
        self.toolButton_trimetric.setEnabled(False)
        self.toolButton_dimetric.setEnabled(False)
        self.toolButton_isometric.setEnabled(False)
        # set axes
        self.roll = 0
        self.pitch = 0
        self.yaw = 0

    def three_d_function(self):
        # set view
        self.view = '3D'
        # set corresponding axis rotations
        self.toolButton_Xroll.setChecked(True)
        self.toolButton_Ypitch.setChecked(True)
        self.toolButton_Zyaw.setChecked(True)
        # hide non corresponding
        self.toolButton_Xroll.setEnabled(True)
        self.toolButton_Ypitch.setEnabled(True)
        self.toolButton_Zyaw.setEnabled(True)
        self.toolButton_trimetric.setEnabled(True)
        self.toolButton_dimetric.setEnabled(True)
        self.toolButton_isometric.setEnabled(True)
        self.isometric_function()

    def x_roll_function(self):
        self.toolButton_Ypitch.setChecked(False)

    def y_pitch_function(self):
        self.toolButton_Xroll.setChecked(False)

    def z_yaw_function(self):
        pass

    def trimetric_function(self):
        # clear other buttons states
        self.toolButton_clicked = 0
        self.toolButton_previous = "trimetric"
        self.toolButton_dimetric.setChecked(False)
        self.toolButton_dimetric.setIcon(QIcon('icons/mode-3d-dimetric-wireframe.png'))
        self.toolButton_isometric.setChecked(False)
        self.toolButton_isometric.setIcon(QIcon('icons/mode-3d-isometric-wireframe.png'))
        # set to 3D mode
        self.toolButton_2D.setChecked(False)
        self.toolButton_3D.setChecked(True)
        # set corresponding axis rotations
        self.toolButton_Xroll.setChecked(True)
        self.toolButton_Ypitch.setChecked(False)
        self.toolButton_Zyaw.setChecked(True)
        # hide non corresponding
        self.toolButton_Xroll.setEnabled(True)
        self.toolButton_Ypitch.setEnabled(True)
        self.toolButton_Zyaw.setEnabled(True)

    def dimetric_function(self):
        # set to 3D mode
        self.toolButton_2D.setChecked(False)
        self.toolButton_3D.setChecked(True)
        # clear other buttons states
        self.toolButton_trimetric.setChecked(False)
        self.toolButton_dimetric.setChecked(False)
        self.toolButton_isometric.setChecked(False)
        self.toolButton_isometric.setIcon(QIcon('icons/mode-3d-isometric-wireframe.png'))
        # if no state set to initial state 1
        if self.toolButton_clicked == 0:
            self.toolButton_clicked = 1
            self.toolButton_previous = "dimetric"
        # if current button and state exists
        elif self.toolButton_previous == "dimetric":
            self.toolButton_clicked += 1
            self.toolButton_previous = "dimetric"
        # if not current button and state exists
        else:
            self.toolButton_previous = "dimetric"
        # max states = 4
        if self.toolButton_clicked > 4:
            self.toolButton_clicked = 1
        # on click change views and button icon
        if self.toolButton_clicked == 1:
            self.toolButton_dimetric.setIcon(QIcon('icons/mode-3d-dimetric-wireframe_1.png'))
            self.yaw = 225
        elif self.toolButton_clicked == 2:
            self.toolButton_dimetric.setIcon(QIcon('icons/mode-3d-dimetric-wireframe_2.png'))
            self.yaw = 315
        elif self.toolButton_clicked == 3:
            self.toolButton_dimetric.setIcon(QIcon('icons/mode-3d-dimetric-wireframe_3.png'))
            self.yaw = 45
        elif self.toolButton_clicked == 4:
            self.toolButton_dimetric.setIcon(QIcon('icons/mode-3d-dimetric-wireframe_4.png'))
            self.yaw = 135
        # set corresponding axis rotations
        self.toolButton_Xroll.setChecked(True)
        self.toolButton_Ypitch.setChecked(False)
        self.toolButton_Zyaw.setChecked(False)
        # hide non corresponding
        self.toolButton_Xroll.setEnabled(True)
        self.toolButton_Ypitch.setEnabled(False)
        self.toolButton_Zyaw.setEnabled(False)
        # set axes
        self.pitch = 0

    def isometric_function(self):
        # set to 3D mode
        self.toolButton_2D.setChecked(False)
        self.toolButton_3D.setChecked(True)
        # clear other buttons states
        self.toolButton_trimetric.setChecked(False)
        self.toolButton_dimetric.setChecked(False)
        self.toolButton_dimetric.setIcon(QIcon('icons/mode-3d-dimetric-wireframe.png'))
        self.toolButton_isometric.setChecked(False)
        # if no state set to initial state 1
        if self.toolButton_clicked == 0:
            self.toolButton_clicked = 1
            self.toolButton_previous = "isometric"
        # if current button and state exists
        elif self.toolButton_previous == "isometric":
            self.toolButton_clicked += 1
            self.toolButton_previous = "isometric"
        # if not current button and state exists
        else:
            self.toolButton_previous = "isometric"
        # max states = 4
        if self.toolButton_clicked > 4:
            self.toolButton_clicked = 1
        # on click change views and button icon
        if self.toolButton_clicked == 1:
            self.toolButton_isometric.setIcon(QIcon('icons/mode-3d-isometric-wireframe_1.png'))
            self.yaw = 225
        elif self.toolButton_clicked == 2:
            self.toolButton_isometric.setIcon(QIcon('icons/mode-3d-isometric-wireframe_2.png'))
            self.yaw = 315
        elif self.toolButton_clicked == 3:
            self.toolButton_isometric.setIcon(QIcon('icons/mode-3d-isometric-wireframe_3.png'))
            self.yaw = 45
        elif self.toolButton_clicked == 4:
            self.toolButton_isometric.setIcon(QIcon('icons/mode-3d-isometric-wireframe_4.png'))
            self.yaw = 135
        # set corresponding axis rotations
        self.toolButton_Xroll.setChecked(False)
        self.toolButton_Ypitch.setChecked(False)
        self.toolButton_Zyaw.setChecked(False)
        # hide non corresponding
        self.toolButton_Xroll.setEnabled(False)
        self.toolButton_Ypitch.setEnabled(False)
        self.toolButton_Zyaw.setEnabled(False)
        # set axes
        self.roll = self.CONST_ISO
        self.pitch = 0

    """Mouse Event filter in openGLWidget"""
    def eventFilter(self, source, event):
        # left button double click
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
                self.mouse_x = event.pos().x()
                self.mouse_y = self.openGLWidget.height() - event.pos().y()
                self.doubleclick = True
                print(self.mouse_x, self.mouse_y, self.doubleclick)
                
        # left button down mouse drag
        if (event.type() == QtCore.QEvent.MouseMove and
                event.buttons() == QtCore.Qt.LeftButton and
                0 <= event.pos().x() <= self.openGLWidget.width() and
                0 <= event.pos().y() <= self.openGLWidget.height() and
                any([self.toolButton_Xroll.isChecked(),
                     self.toolButton_Ypitch.isChecked(),
                     self.toolButton_Zyaw.isChecked()])):
            # change settings
            if self.toolButton_Zyaw.isChecked():
                self.toolButton_isometric.setChecked(False)
                self.toolButton_dimetric.setChecked(True)
            else:
                self.toolButton_isometric.setChecked(False)
                self.toolButton_dimetric.setChecked(False)
            # get current
            current = pygame.Vector2(event.pos().x(), event.pos().y() * -1)
            # on initial click set to current
            if self.first:
                QApplication.setOverrideCursor(QCursor(QtCore.Qt.ClosedHandCursor))
                self.previous = current
                self.first = False
            # calculate change in xy
            change_in_xy = round(current - self.previous)
            # pos or neg x direction
            if self.toolButton_Xroll.isChecked():
                self.roll += change_in_xy.y * self.sensitivity
                # rotation min max
                if self.roll >= 360:
                    self.roll -= 360
                elif self.roll < 0:
                    self.roll += 360
            elif self.toolButton_Ypitch.isChecked():
                self.pitch += change_in_xy.y * self.sensitivity
                # rotation min max
                if self.pitch >= 360:
                    self.pitch -= 360
                elif self.pitch < 0:
                    self.pitch += 360
            if self.toolButton_Zyaw.isChecked():
                # check for 2D or 3D view
                if self.toolButton_2D.isChecked():
                    self.yaw += change_in_xy.x * self.sensitivity
                elif self.toolButton_3D.isChecked():
                    self.yaw -= change_in_xy.x * self.sensitivity
                # rotation min max
                if self.yaw >= 360:
                    self.yaw -= 360
                elif self.yaw < 0:
                    self.yaw += 360
            # set current to previous
            self.previous = current
        # on release leave drag event
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            self.first = True
            QApplication.restoreOverrideCursor()
            
        # real time mouse position
        if event.type() == QtCore.QEvent.MouseMove:
            self.real_time_mouse_x = event.pos().x()
            self.real_time_mouse_y = self.openGLWidget.height() - event.pos().y()

        # wheel event
        if event.type() == QtCore.QEvent.Wheel:
            scroll = event.angleDelta()
            if scroll.y() > 0:
                if self.zoom > self.sensitivity:
                    self.zoom -= self.sensitivity
            else:
                self.zoom += self.sensitivity

        return super(MainWindow, self).eventFilter(source, event)
