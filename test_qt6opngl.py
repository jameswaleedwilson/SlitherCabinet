
# main_app.py
from PyQt6 import QtWidgets, uic
import sys
from OpenGL.GL import *
from my_opengl_widget import MyOpenGLWidget # Import your custom widget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.openGLWidget = None
        uic.loadUi('MainWindowqt6b.ui', self) # Load your .ui file
        self.openGLWidget.initializeGL = self.initialise_gl
        self.openGLWidget.paintGL = self.paint_gl


    def initialise_gl(self):
        glEnable(GL_DEPTH_TEST)
        #glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black

    def resizeGL(self, w, h):
        pass# glViewport(0, 0, w, h)

    def paint_gl(self):
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Your OpenGL drawing commands here (e.g., drawing a triangle)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(-0.5, -0.5)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(0.5, -0.5)
        glColor3f(0.0, 0.0, 1.0)
        glVertex2f(0.0, 0.5)
        glEnd()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())