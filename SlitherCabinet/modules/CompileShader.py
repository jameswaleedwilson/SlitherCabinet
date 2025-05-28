from .utilities import *


class CompileShader:

    def __init__(self, vertex_shader, fragment_shader, geometry_shader=None):
        if geometry_shader is not None:
            self.link_shader = link_shader(open(vertex_shader).read(),
                                           open(fragment_shader).read(),
                                           open(geometry_shader).read())
        else:
            self.link_shader = link_shader(open(vertex_shader).read(),
                                           open(fragment_shader).read())

    def use(self):
        glUseProgram(self.link_shader)
