from .load_default_vao import *
from .load_custom_vao import *
import pygame
from .utilities import *


# need error checking
class LoadVBO(LoadDefaultVAO, LoadCustomVAO):
    def __init__(self, obj_filename, image_front,
                 draw_type=GL_TRIANGLES,
                 # local once off change
                 location=pygame.Vector3(0, 0, 0),
                 rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 std_scale=pygame.Vector3(1, 1, 1),
                 # animation
                 move_rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),

                 shader=None,
                 image_back=None,
                 identifier=(0, 0, 0)):

        # change the above to pass colour through
        coordinates, triangles, uvs, uvs_ind, normals, normal_ind, texture_1, texture_2 = self.load_mesh(obj_filename, image_front, image_back)
        vertices = format_vertices(coordinates, triangles)
        vertex_normals = format_vertices(normals, normal_ind)
        vertex_uvs = format_vertices(uvs, uvs_ind)
        textures = np.stack((texture_1, texture_2), axis=1)
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
                         shader=shader,
                         identifier=identifier,
                         vertex_textures=textures)

    @staticmethod
    def load_mesh(filename, image_front, image_back):
        vertices = []
        triangles = []
        normals = []
        normal_ind = []
        uvs = []
        uvs_ind = []
        # https://www.khronos.org/opengl/wiki/Array_Texture upgrade multiple textures to arrays
        material_library = None
        current_material = 0
        texture_1 = []
        texture_2 = []

        with open(filename) as obj_file:
            line_obj_file = obj_file.readline()
            while line_obj_file:

                if line_obj_file[:6] == "mtllib":
                    material_library = line_obj_file[7:]
                    print("material file exists")

                if line_obj_file[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line_obj_file[2:].split()]
                    vertices.append((vx, vy, vz))

                if line_obj_file[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line_obj_file[3:].split()]
                    normals.append((vx, vy, vz))

                if line_obj_file[:2] == "vt":
                    vx, vy = [float(value) for value in line_obj_file[2:].split()]
                    uvs.append((vx, vy))

                if line_obj_file[:6] == "usemtl":
                    current_material += 1
                    print("found new material")

                if line_obj_file[:2] == "f ":
                    t1, t2, t3 = [value for value in line_obj_file[2:].split()]

                    triangles.append([int(value) for value in t1.split('/')][0] - 1)
                    triangles.append([int(value) for value in t2.split('/')][0] - 1)
                    triangles.append([int(value) for value in t3.split('/')][0] - 1)

                    uvs_ind.append([int(value) for value in t1.split('/')][1] - 1)
                    uvs_ind.append([int(value) for value in t2.split('/')][1] - 1)
                    uvs_ind.append([int(value) for value in t3.split('/')][1] - 1)

                    normal_ind.append([int(value) for value in t1.split('/')][2] - 1)
                    normal_ind.append([int(value) for value in t2.split('/')][2] - 1)
                    normal_ind.append([int(value) for value in t3.split('/')][2] - 1)

                    # if a material library does not exist use front_image ***** update when no image required default to default color
                    if material_library is None:
                        texture_1.append(int(1))
                        texture_1.append(int(1))
                        texture_1.append(int(1))

                        if image_back is None:
                            texture_2.append(int(0))
                            texture_2.append(int(0))
                            texture_2.append(int(0))
                        else:
                            texture_2.append(int(2))
                            texture_2.append(int(2))
                            texture_2.append(int(2))

                line_obj_file = obj_file.readline()
        #print(uvs_ind)
        #print(texture_1)
        #print(texture_2)
        return vertices, triangles, uvs, uvs_ind, normals, normal_ind, texture_1, texture_2
