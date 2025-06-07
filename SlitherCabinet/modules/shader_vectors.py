from OpenGL.GL import *
import numpy as np


class ShaderVectors:
    def __init__(self, vector_type, vector_data):
        self.vector_type = vector_type
        self.vector_data = vector_data
        # CREATE VBO
        # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glGenBuffers.xml
        self.vector_location = glGenBuffers(1)
        self.load()

    def load(self):
        vector_data = np.array(self.vector_data, np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.vector_location)
        glBufferData(GL_ARRAY_BUFFER, vector_data.ravel(), GL_STATIC_DRAW)

    def find_variable(self, vector_location, vector_name):
        vector_location = glGetAttribLocation(vector_location, vector_name)
        glBindBuffer(GL_ARRAY_BUFFER, self.vector_location)
        if self.vector_type == "vec4":
            glVertexAttribPointer(vector_location, 4, GL_FLOAT, False, 0, None)
        elif self.vector_type == "vec3":
            glVertexAttribPointer(vector_location, 3, GL_FLOAT, False, 0, None)
        elif self.vector_type == "vec2":
            glVertexAttribPointer(vector_location, 2, GL_FLOAT, False, 0, None)
        elif self.vector_type == "ivec3":
            glVertexAttribPointer(vector_location, 3, GL_INT, False, 0, None)

        glEnableVertexAttribArray(vector_location)
