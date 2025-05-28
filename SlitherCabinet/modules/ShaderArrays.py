from OpenGL.GL import *
import numpy as np


class ShaderArrays:
    def __init__(self, vector_type, vector_data):
        self.vector_type = vector_type
        self.vector_data = vector_data
        # CREATE VBO
        # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glGenBuffers.xml
        self.array_location = glGenBuffers(1)
        self.load()

    def load(self):
        vector_data = np.array(self.vector_data, np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.array_location)
        glBufferData(GL_ARRAY_BUFFER, vector_data.ravel(), GL_STATIC_DRAW)

    def find_variable(self, vector_location, vector_name):
        vector_location = glGetAttribLocation(vector_location, vector_name)
        glBindBuffer(GL_ARRAY_BUFFER, self.array_location)
        if self.vector_type == "vec4":
            glVertexAttribPointer(vector_location, 4, GL_FLOAT, False, 0, None)
        elif self.vector_type == "vec3":
            glVertexAttribPointer(vector_location, 3, GL_FLOAT, False, 0, None)
        elif self.vector_type == "vec2":
            glVertexAttribPointer(vector_location, 2, GL_FLOAT, False, 0, None)
        elif self.vector_type == "ivec3":
            glVertexAttribPointer(vector_location, 3, GL_INT, False, 0, None)

        glEnableVertexAttribArray(vector_location)

    def modify(self, new_data, array_index):
        # update a portion of data
        data_offset = array_index * new_data.itemsize
        glBindBuffer(GL_ARRAY_BUFFER, self.array_location)
        glBufferSubData(GL_ARRAY_BUFFER, data_offset, new_data.nbytes, new_data)
