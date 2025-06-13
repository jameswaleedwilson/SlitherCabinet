# Operating system
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# Python packages
import math
import pygame

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QApplication
# Local modules
"""None"""


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.real_time_mouse_y = None
        self.real_time_mouse_x = None
        self.doubleclick = None
        self.mouse_y = None
        self.mouse_x = None

        # remove grid and axes
        self.grid = None
        self.axes = None
        self.CONST_ISO = math.degrees(math.asin(math.sqrt(2 / 3)))  # ~54.73 degrees
        # remove default window frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        # left button mouse drag for 3D rotation
        self.first = True
        self.previous = pygame.Vector2(0, 0)
        self.rotation_sensitivity = 1
        self.camera_focal_point_sensitivity = 0.01
        self.roll = None
        self.pitch = None
        self.yaw = None
        self.zoom = None
        # button state
        self.toolButton_clicked = 0
        self.toolButton_previous = ""
        self.toolButton_dimetric_clicked = 0
        self.toolButton_isometric_clicked = 0
        # middle button mouse drag for camera focus
        self.camera_focal_point = pygame.Vector3(300, 150, 0)


        uic.loadUi('ui/MainWindow.ui', self)
        self.verticalSlider_glClipPlane.valueChanged.connect(self.gl_clip_plane_function)
        self.verticalSlider_glClipPlane_value = None
        self.label_clip.setText('Clipped ' + str(self.verticalSlider_glClipPlane_value))

        # window setting for resize / maximize / minimize
        self.window_settings_minimized = None
        self.toolButton_minimize.clicked.connect(self.minimize_function)
        self.toolButton_maximize.clicked.connect(self.maximize_function)
        self.toolButton_close.clicked.connect(self.close_function)
        # Environment
        # View
        self.view = '3D'
        self.yaw2D = 0
        self.toolButton_axes.clicked.connect(self.axes_function)
        self.toolButton_grid.clicked.connect(self.grid_function)
        self.toolButton_2D.clicked.connect(self.two_d_function)
        self.toolButton_3D.clicked.connect(self.three_d_function)
        self.toolButton_trimetric.clicked.connect(self.trimetric_function)
        self.toolButton_dimetric.clicked.connect(self.dimetric_function)
        self.toolButton_isometric.clicked.connect(self.isometric_function)
        self.toolButton_Xroll.clicked.connect(self.x_roll_function)
        self.toolButton_Ypitch.clicked.connect(self.y_pitch_function)
        self.toolButton_Zyaw.clicked.connect(self.z_yaw_function)

    def setup_ui(self):
        pass

    def initialise_gl(self):
        pass

    def camera_init(self):
        pass

    def paintGL(self):
        pass

    def minimize_function(self):
        pass

    def maximize_function(self):
        pass

    def close_function(self):
        pass

    def axes_function(self, event):
        self.axes = event

    def grid_function(self, event):
        self.grid = event

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

    def gl_clip_plane_function(self, value):
        self.verticalSlider_glClipPlane_value = value
        self.label_clip.setText('Clipped ' + str(value))

    def eventFilter(self, source, event):
        # left button double click
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
                self.mouse_x = event.pos().x()
                self.mouse_y = self.openGLWidget.height() - event.pos().y()
                self.doubleclick = True

        # left button down mouse drag -> 3D rotation
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
            change_in_xy = current - self.previous
            # pos or neg x direction
            if self.toolButton_Xroll.isChecked():
                self.roll += change_in_xy.y * self.rotation_sensitivity
                # rotation min max
                if self.roll >= 360:
                    self.roll -= 360
                elif self.roll < 0:
                    self.roll += 360
            elif self.toolButton_Ypitch.isChecked():
                self.pitch += change_in_xy.y * self.rotation_sensitivity
                # rotation min max
                if self.pitch >= 360:
                    self.pitch -= 360
                elif self.pitch < 0:
                    self.pitch += 360
            if self.toolButton_Zyaw.isChecked():
                # check for 2D or 3D view
                if self.toolButton_2D.isChecked():
                    self.yaw += change_in_xy.x * self.rotation_sensitivity
                elif self.toolButton_3D.isChecked():
                    self.yaw -= change_in_xy.x * self.rotation_sensitivity
                # rotation min max
                if self.yaw >= 360:
                    self.yaw -= 360
                elif self.yaw < 0:
                    self.yaw += 360
            # set current to previous
            self.previous = current

        # middle (scroll) button down mouse drag -> camera focal point
        if (event.type() == QtCore.QEvent.MouseMove and
                event.buttons() == QtCore.Qt.MiddleButton and
                0 <= event.pos().x() <= self.openGLWidget.width() and
                0 <= event.pos().y() <= self.openGLWidget.height()):
            # get current
            current = pygame.Vector2(event.pos().x(), event.pos().y() * -1)
            # on initial click set to current
            if self.first:
                QApplication.setOverrideCursor(QCursor(QtCore.Qt.ClosedHandCursor))
                self.previous = current
                self.first = False
            # calculate change in xy
            change_in_xy = current - self.previous
            self.camera_focal_point.x += change_in_xy.x * self.camera_focal_point_sensitivity * -1
            self.camera_focal_point.y += change_in_xy.y * self.camera_focal_point_sensitivity * -1
            print(change_in_xy)
            print(self.camera_focal_point)

        # on release leave drag event
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            self.first = True
            QApplication.restoreOverrideCursor()
            
        # real time mouse position -> pixel picking
        if event.type() == QtCore.QEvent.MouseMove:
            self.real_time_mouse_x = event.pos().x()
            self.real_time_mouse_y = self.openGLWidget.height() - event.pos().y()

        # wheel event
        if event.type() == QtCore.QEvent.Wheel:
            scroll = event.angleDelta()
            if scroll.y() > 0:
                if self.zoom > self.rotation_sensitivity:
                    self.zoom -= self.rotation_sensitivity
            else:
                self.zoom += self.rotation_sensitivity

        return super(MainWindow, self).eventFilter(source, event)
