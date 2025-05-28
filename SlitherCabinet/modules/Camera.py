from .TransformationMatrices import *
from .ShaderUniforms import *


class Camera:
    def __init__(self, screen_width, screen_height):
        self.view_mat = None
        self.init_zoom = 1
        self.near_plane = 1000
        self.far_plane = -1000
        # 2D view looking down z, +y up +x right
        self.transformation2D = identity_mat()
        # 3d view looking down x, +y right, +z up
        self.transformation3D = rotate(identity_mat(), -270, "z", False)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def rotate(self, roll, pitch, yaw, view):
        if view == '2D':
            self.view_mat = self.transformation2D
            self.view_mat = translate(self.view_mat, 300, 150, 0)
            self.view_mat = rotate(self.view_mat, -yaw, "z", True)
        else:
            self.view_mat = self.transformation3D
            self.view_mat = translate(self.view_mat, 150, -300, 0)
            self.view_mat = rotate(self.view_mat, yaw, "z", True)
            self.view_mat = rotate(self.view_mat, roll, "x", True)
            self.view_mat = rotate(self.view_mat, pitch, "y", True)

    def update(self, program_id, zoom, roll, pitch, yaw, view):

        self.rotate(roll, pitch, yaw, view)

        projection_mat = orthographic_mat(self.screen_width / self.screen_height, self.near_plane,
                                          self.far_plane, zoom)

        projection = ShaderUniforms("mat4", projection_mat)
        projection.find_variable(program_id, "projection_mat")
        projection.load()

        view = ShaderUniforms("mat4", self.view_mat)
        view.find_variable(program_id, "view_mat")
        view.load()

        return self.view_mat
