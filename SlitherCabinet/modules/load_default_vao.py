import pygame
from .shader_vectors import *
from .load_texture import LoadTexture
from .shader_uniforms import *
from .transformation_matrices import *


class LoadDefaultVAO:
    def __init__(self, vertices,
                 # manually assigned texture if not using mtl
                 image_front=None,
                 image_back=None,
                 #vertex specific data
                 vertex_normals=None,
                 vertex_uvs=None,
                 vertex_colors=None,
                 vertex_textures=None,
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

        self.shader = shader
        self.vertices = vertices
        self.vertex_normals = vertex_normals
        self.vertex_colors = vertex_colors
        self.vertex_uvs = vertex_uvs
        self.draw_type = draw_type
        #self.background_color = (45.0 / 255.0, 45.0 / 255.0, 45.0 / 255.0, 1.0)
        self.identifier = identifier
        self.vertex_textures = vertex_textures

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

        if self.vertex_textures is not None:
            vertex_textures = ShaderVectors("vec2", self.vertex_textures)
            vertex_textures.find_variable(self.shader.link_shader, "vertex_texture")

        # do not change order
        self.model_mat = identity_mat()
        self.model_mat = rotate_a(self.model_mat, rotation.angle, rotation.axis)
        self.model_mat = translate(self.model_mat, translation.x, translation.y, translation.z)
        self.model_mat = scale3(self.model_mat, std_scale.x, std_scale.y, std_scale.z)

        self.move_rotation = move_rotation
        self.move_translate = move_translate
        self.move_scale = move_scale

        self.texture_front = None
        if image_front is not None:
            self.image = LoadTexture(image_front)
            self.texture_front = ShaderUniforms("sampler2D", [self.image.id, 1])

        self.texture_back = None
        if image_back is not None:
            self.image = LoadTexture(image_back)
            self.texture_back = ShaderUniforms("sampler2D", [self.image.id, 2])

    def draw_default_fbo(self, camera, lights, zoom, roll, pitch, yaw, view,
                         current_pixel_color=None,
                         clip_z=None,
                         new_location=None):

        self.shader.use()

        # switcher '0' draws to the DEFAULT FBO - (frame buffer object)
        fbo_switcher = ShaderUniforms("int1", 0)
        fbo_switcher.find_variable(self.shader.link_shader, "fbo_switcher")
        fbo_switcher.load()

        #
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

        if self.texture_front is not None:
            self.texture_front.find_variable(self.shader.link_shader, "tex_front")
            self.texture_front.load()

        if self.texture_back is not None:
            self.texture_back.find_variable(self.shader.link_shader, "tex_back")
            self.texture_back.load()

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