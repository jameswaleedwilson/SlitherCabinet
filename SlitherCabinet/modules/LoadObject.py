from .LoadDefaultFBO import *
from .LoadCustomFBO import *
import pygame
from .utilities import *


# need error checking

class LoadObject(LoadDefaultFBO, LoadCustomFBO):
    def __init__(self, obj_filename, image_front,
                 draw_type=GL_TRIANGLES,
                 location=pygame.Vector3(0, 0, 0),
                 rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 # this may be a double up with move scale???
                 # no, this is initial position
                 std_scale=pygame.Vector3(1, 1, 1),
                 move_rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),
                 shader=None,
                 image_back=None):

        # change the above to pass colour through
        coordinates, triangles, uvs, uvs_ind, normals, normal_ind = self.load_drawing(obj_filename)
        vertices = format_vertices(coordinates, triangles)
        # print(vertices)
        vertex_normals = format_vertices(normals, normal_ind)
        vertex_uvs = format_vertices(uvs, uvs_ind)
        texture = []
        for i in range(len(vertices)):
            texture.append(1)
            texture.append(1)
            texture.append(1)
        super().__init__(vertices,
                         image_front=image_front,
                         image_back=image_back,
                         vertex_normals=vertex_normals,
                         vertex_uvs=vertex_uvs,
                         vertex_colors=texture,
                         draw_type=draw_type,
                         translation=location,
                         rotation=rotation,
                         std_scale=std_scale,
                         move_rotation=move_rotation,
                         move_translate=move_translate,
                         move_scale=move_scale,
                         shader=shader)

    @staticmethod
    def load_drawing(filename):
        vertices = []
        triangles = []
        normals = []
        normal_ind = []
        uvs = []
        uvs_ind = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))

                if line[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line[3:].split()]
                    normals.append((vx, vy, vz))

                if line[:2] == "vt":
                    vx, vy = [float(value) for value in line[2:].split()]
                    uvs.append((vx, vy))

                if line[:2] == "f ":
                    t1, t2, t3 = [value for value in line[2:].split()]

                    triangles.append([int(value) for value in t1.split('/')][0] - 1)
                    triangles.append([int(value) for value in t2.split('/')][0] - 1)
                    triangles.append([int(value) for value in t3.split('/')][0] - 1)

                    uvs_ind.append([int(value) for value in t1.split('/')][1] - 1)
                    uvs_ind.append([int(value) for value in t2.split('/')][1] - 1)
                    uvs_ind.append([int(value) for value in t3.split('/')][1] - 1)

                    normal_ind.append([int(value) for value in t1.split('/')][2] - 1)
                    normal_ind.append([int(value) for value in t2.split('/')][2] - 1)
                    normal_ind.append([int(value) for value in t3.split('/')][2] - 1)

                line = fp.readline()
        return vertices, triangles, uvs, uvs_ind, normals, normal_ind
