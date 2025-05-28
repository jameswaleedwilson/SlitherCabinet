from OpenGL.GL import *


class ShaderUniforms:
    def __init__(self, uniform_type, uniform_data):
        self.uniform_type = uniform_type
        self.uniform_data = uniform_data
        self.uniform_location = None

    def find_variable(self, uniform_location, uniform_name):
        self.uniform_location = glGetUniformLocation(uniform_location, uniform_name)

    def load(self):
        if self.uniform_type == "int1":
            glUniform1i(self.uniform_location,
                        self.uniform_data)
        elif self.uniform_type == "vec3":
            glUniform3f(self.uniform_location,
                        self.uniform_data[0],
                        self.uniform_data[1],
                        self.uniform_data[2])
        elif self.uniform_type == "vec4":
            glUniform4f(self.uniform_location,
                        self.uniform_data[0],
                        self.uniform_data[1],
                        self.uniform_data[2],
                        self.uniform_data[3])
        elif self.uniform_type == "mat4":
            glUniformMatrix4fv(self.uniform_location, 1, GL_TRUE, self.uniform_data)
        elif self.uniform_type == "sampler2D":
            texture_obj, texture_unit = self.uniform_data
            glActiveTexture(GL_TEXTURE0 + texture_unit)
            glBindTexture(GL_TEXTURE_2D, texture_obj)
            glUniform1i(self.uniform_location, texture_unit)
        elif self.uniform_type == "ivec3":
            glUniform3iv(self.uniform_location, 1, self.uniform_data)
