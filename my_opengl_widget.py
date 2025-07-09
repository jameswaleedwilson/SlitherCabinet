# my_opengl_widget.py
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *

class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0) # Set background color to black

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Your OpenGL drawing commands here (e.g., drawing a triangle)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(-0.5, -0.5)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(0.5, -0.5)
        glColor3f(0.0, 0.0, 1.0)
        glVertex2f(0.0, 0.5)
        glEnd()
