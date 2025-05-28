import pygame
from .TransformationMatrices import *
from .ShaderUniforms import *


class Light:
    def __init__(self, position=pygame.Vector3(0, 0, 0), color=pygame.Vector3(1, 1, 1), light_number=0,
                 move_with_camera=False):
        # self.transformation = identity_mat()
        self.move_with_camera = move_with_camera
        self.position = position
        self.color = color
        self.light_variable = "light_data[" + str(light_number) + "].position"
        self.color_variable = "light_data[" + str(light_number) + "].color"

    def update(self, program_id, view_mat):

        if self.move_with_camera:
            view_mat = np.array(view_mat)
            position = np.array(np.append(self.position, 1))
            position = view_mat.dot(position)
            position = (position[0], position[1], position[2])

            light_pos = ShaderUniforms("vec3", position)
            light_pos.find_variable(program_id, self.light_variable)
            light_pos.load()
        else:
            light_pos = ShaderUniforms("vec3", self.position)
            light_pos.find_variable(program_id, self.light_variable)
            light_pos.load()

        color = ShaderUniforms("vec3", self.color)
        color.find_variable(program_id, self.color_variable)
        color.load()
