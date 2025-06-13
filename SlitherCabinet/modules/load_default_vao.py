# Operating system
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# Python packages
import pygame
# Local modules
from .shader_vectors import *
from .load_texture import LoadTexture
from .shader_uniforms import *
from .transformation_matrices import *


class LoadDefaultVAO:
    def __init__(self, vertices,
                 #vertex specific data
                 vertex_normals=None,
                 vertex_uvs=None,
                 vertex_colors=None,
                 image_ids=None,
                 image_front_array=None,
                 image_back=None,
                 draw_type=GL_TRIANGLES,
                 # static
                 translation=pygame.Vector3(0.0, 0.0, 0.0),
                 rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 std_scale=pygame.Vector3(1, 1, 1),
                 # dynamic
                 move_rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),
                 # shader
                 shader=None,
                 # pixel picking rgb identifier
                 identifier=None):

        self.vertices = vertices
        self.vertex_normals = vertex_normals
        self.vertex_uvs = vertex_uvs
        self.vertex_colors = vertex_colors
        self.vertex_textures_id = image_ids

        self.draw_type = draw_type
        self.shader = shader
        self.identifier = identifier

        # CREATE VAO
        # A Vertex Array Object (VAO) is an object which contains one or more Vertex Buffer Objects
        # https://www.khronos.org/opengl/wiki/Tutorial2:_VAOs,_VBOs,_Vertex_and_Fragment_Shaders_(C_/_SDL)
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        if self.vertices is not None:
            vertices = ShaderVectors("vec3", self.vertices)
            vertices.find_variable(self.shader.link_shader, "vertices")

        if self.vertex_colors is not None:
            vertex_colors = ShaderVectors("vec3", self.vertex_colors)
            vertex_colors.find_variable(self.shader.link_shader, "vertex_color")

        if self.vertex_normals is not None:
            vertex_normals = ShaderVectors("vec3", self.vertex_normals)
            vertex_normals.find_variable(self.shader.link_shader, "vertex_normal")

        if self.vertex_uvs is not None:
            vertex_uvs = ShaderVectors("vec2", self.vertex_uvs)
            vertex_uvs.find_variable(self.shader.link_shader, "vertex_uv")

        if self.vertex_textures_id is not None:
            image_ids = ShaderVectors("vec2", self.vertex_textures_id)
            image_ids.find_variable(self.shader.link_shader, "vertex_texture_id")

        # do not change order
        self.model_mat = identity_mat()
        self.model_mat = rotate_a(self.model_mat, rotation.angle, rotation.axis)
        self.model_mat = translate(self.model_mat, translation.x, translation.y, translation.z)
        self.model_mat = scale3(self.model_mat, std_scale.x, std_scale.y, std_scale.z)

        self.move_rotation = move_rotation
        self.move_translate = move_translate
        self.move_scale = move_scale

        # convert image -> texture
        self.vertex_texture_front_array = {}
        image_count = 1
        if image_front_array is not None:
            for img in image_front_array:
                texture = LoadTexture(img)
                self.vertex_texture_front_array[f"texture{image_count}"] = ShaderUniforms("sampler2D", [texture.id, image_count])
                image_count += 1

        self.image_back = None
        if image_back is not None:
            img = LoadTexture(image_back)
            self.image_back = ShaderUniforms("sampler2D", [img.id, image_count])

    def draw_default_fbo(self, camera, lights, zoom, roll, pitch, yaw, view,
                         current_pixel_color=None,
                         clip_z=None,
                         new_location=None):

        self.shader.use()

        # switcher '0' draws to the DEFAULT FBO - (frame buffer object)
        fbo_switcher = ShaderUniforms("int1", 0)
        fbo_switcher.find_variable(self.shader.link_shader, "fbo_switcher")
        fbo_switcher.load()

        # pixel picking rgb identifier
        if self.identifier is not None:
            identifier = self.identifier
            identifier = ShaderUniforms("ivec3", identifier)
            identifier.find_variable(self.shader.link_shader,"identifier")
            identifier.load()

        # current selected read pixel
        if current_pixel_color is not None:
            current_pixel_color = ShaderUniforms("ivec3", current_pixel_color)
            current_pixel_color.find_variable(self.shader.link_shader, "current_pixel_color")
            current_pixel_color.load()

        if new_location is not None:
            self.move_translate = new_location

        view_mat = camera.update(self.shader.link_shader, zoom, roll, pitch, yaw, view)

        if lights is not None:
            for light in lights:
                light.update(self.shader.link_shader, view_mat)

        texture_count = 1
        for texture in self.vertex_texture_front_array.values():
            texture.find_variable(self.shader.link_shader, "tex_front" + str(texture_count))
            texture.load()
            texture_count += 1

        if self.image_back is not None:
            self.image_back.find_variable(self.shader.link_shader, "tex_back")
            self.image_back.load()

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