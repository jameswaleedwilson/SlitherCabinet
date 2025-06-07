from .utilities import *


class CompileShader:

    def __init__(self, vertex_shader, fragment_shader):
        self.link_shader = link_shader(open(vertex_shader).read(), open(fragment_shader).read())

    def use(self):
        glUseProgram(self.link_shader)
