from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from .ShaderArrays import *
from .LoadTexture import LoadTexture
from .ShaderUniforms import *
from .TransformationMatrices import *


class LoadCustomFBO:
    def __init__(self, vertices,
                 image_front=None,
                 image_back=None,
                 vertex_normals=None,
                 vertex_uvs=None,
                 vertex_colors=None,
                 draw_type=GL_TRIANGLES,
                 translation=pygame.Vector3(0.0, 0.0, 0.0),
                 rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 std_scale=pygame.Vector3(1, 1, 1),
                 move_rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),
                 shader=None):
        self.shader = shader
        self.vertices = vertices
        self.vertex_normals = vertex_normals
        self.vertex_colors = vertex_colors
        self.vertex_uvs = vertex_uvs
        self.draw_type = draw_type
        self.background_color = (45.0 / 255.0, 45.0 / 255.0, 45.0 / 255.0, 1.0)

        # CREATE VAO
        # A Vertex Array Object (VAO) is an object which contains one or more Vertex Buffer Objects
        # https://www.khronos.org/opengl/wiki/Tutorial2:_VAOs,_VBOs,_Vertex_and_Fragment_Shaders_(C_/_SDL)
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        if self.vertices is not None:
            vertices = ShaderArrays("vec3", self.vertices)
            vertices.find_variable(self.shader.link_shader, "vertices")

        if self.vertex_colors is not None:
            vertex_colors = ShaderArrays("vec3", self.vertex_colors)
            vertex_colors.find_variable(self.shader.link_shader, "vertex_color")

        if self.vertex_normals is not None:
            vertex_normals = ShaderArrays("vec3", self.vertex_normals)
            vertex_normals.find_variable(self.shader.link_shader, "vertex_normal")

        if self.vertex_uvs is not None:
            vertex_uvs = ShaderArrays("vec2", self.vertex_uvs)
            vertex_uvs.find_variable(self.shader.link_shader, "vertex_uv")

        # do not change order
        self.model_mat = identity_mat()
        self.model_mat = rotate_a(self.model_mat, rotation.angle, rotation.axis)
        self.model_mat = translate(self.model_mat, translation.x, translation.y, translation.z)
        self.model_mat = scale3(self.model_mat, std_scale.x, std_scale.y, std_scale.z)

        self.move_rotation = move_rotation
        self.move_translate = move_translate
        self.move_scale = move_scale

    def draw_custom_fbo(self, camera, zoom, roll, pitch, yaw, view,
                        object_color_identifier_custom_fbo=None,
                        current_pixel_color=None,
                        clip_z=None):

        self.shader.use()

        # switcher '0' draws to the DEFAULT FBO - (frame buffer object)
        fbo_switcher = ShaderUniforms("int1", 1)
        fbo_switcher.find_variable(self.shader.link_shader, "fbo_switcher")
        fbo_switcher.load()

        #
        if object_color_identifier_custom_fbo is not None:
            object_color_identifier_custom_fbo = ShaderUniforms("ivec3", object_color_identifier_custom_fbo)
            object_color_identifier_custom_fbo.find_variable(self.shader.link_shader, "object_color_identifier_custom_fbo")
            object_color_identifier_custom_fbo.load()

        # current selected read pixel
        if current_pixel_color is not None:
            current_pixel_color = ShaderUniforms("ivec3", current_pixel_color)
            current_pixel_color.find_variable(self.shader.link_shader, "current_pixel_color")
            current_pixel_color.load()

        camera.update(self.shader.link_shader, zoom, roll, pitch, yaw, view)

        if clip_z is not None:
            clip_plane = ShaderUniforms("vec4", (0.0, 0.0, -1.0, clip_z))
            clip_plane.find_variable(self.shader.link_shader, "clip_plane")
            clip_plane.load()

        model_mat = rotate_a(self.model_mat, self.move_rotation.angle, self.move_rotation.axis)
        model_mat = translate(model_mat, self.move_translate.x, self.move_translate.y, self.move_translate.z)
        model_mat = scale3(model_mat, self.move_scale.x, self.move_scale.y, self.move_scale.z)

        model = ShaderUniforms("mat4", model_mat)
        model.find_variable(self.shader.link_shader, "model_mat")
        model.load()

        glBindVertexArray(self.VAO)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
