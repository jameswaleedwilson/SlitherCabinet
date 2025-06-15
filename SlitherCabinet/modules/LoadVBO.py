# Operating system
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# Python packages
"""None"""
# Local modules
from .load_default_vao import *
from .load_custom_vao import *
from .utilities import *


# need error checking
class LoadVBO(LoadDefaultVAO, LoadCustomVAO):
    def __init__(self, obj_filename,
                 obj_dimensions=None,
                 image_front=None,
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

        # return formated data from raw obj
        (coordinates,
         triangles,
         uvs,
         uvs_ind,
         normals,
         normal_ind,
         image_front_id,
         image_back_id,
         image_front_array,
         image_back) = self.load_mesh(obj_filename, image_front, image_back, obj_dimensions)

        vertices = format_vertices(coordinates, triangles)
        vertex_normals = format_vertices(normals, normal_ind)
        vertex_uvs = format_vertices(uvs, uvs_ind)
        image_ids = np.stack((image_front_id, image_back_id), axis=1)

        # default color if no texture or color is given
        default_color = []
        for i in range(len(vertices)):
            default_color.append(1)
            default_color.append(1)
            default_color.append(1)

        super().__init__(vertices,
                         vertex_normals=vertex_normals,
                         vertex_uvs=vertex_uvs,
                         vertex_colors=default_color,
                         draw_type=draw_type,
                         translation=location,
                         rotation=rotation,
                         std_scale=std_scale,
                         move_rotation=move_rotation,
                         move_translate=move_translate,
                         move_scale=move_scale,
                         shader=shader,
                         identifier=identifier,
                         image_ids=image_ids,
                         image_front_array=image_front_array,
                         image_back=image_back)

    @staticmethod
    def load_mesh(filename, image_front, image_back, obj_dimensions):
        vertices = []
        triangles = []
        normals = []
        # normal_indices
        normal_ind = []
        uvs = []
        # uvs_indices
        uvs_ind = []
        # https://www.khronos.org/opengl/wiki/Array_Texture upgrade multiple textures to arrays ????
        material_library = None
        image_count = 0
        image_front_id = []
        image_back_id = []
        image_front_array = []

        with open(filename) as obj_file:
            line_obj_file = obj_file.readline()
            while line_obj_file:

                if line_obj_file[:6] == "mtllib":
                    # store material library name .mtl
                    material_library = "meshesOBJ/" + line_obj_file[7:-1]

                if line_obj_file[:2] == "v ":
                    vx, vy, vz = [value for value in line_obj_file[2:].split()]
                    if vx == "x":
                        vx = obj_dimensions[0]
                    if vy == "y":
                        vy = obj_dimensions[1]
                    if vz == "z":
                        vz = obj_dimensions[2]
                    vx, vy, vz = float(vx), float(vy), float(vz)
                    vertices.append((vx, vy, vz))

                if line_obj_file[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line_obj_file[3:].split()]
                    normals.append((vx, vy, vz))

                if line_obj_file[:2] == "vt":
                    vx, vy = [float(value) for value in line_obj_file[2:].split()]
                    uvs.append((vx, vy))

                if line_obj_file[:6] == "usemtl":
                    image_count += 1

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

                    # use front_image
                    if image_front is not None:
                        image_front_id.append(int(1))
                        image_front_id.append(int(1))
                        image_front_id.append(int(1))
                    elif material_library is not None:
                        # image_front does not exist use mtl library
                        image_front_id.append(int(image_count))
                        image_front_id.append(int(image_count))
                        image_front_id.append(int(image_count))
                    else:
                        # otherwise default color
                        image_front_id.append(int(0))
                        image_front_id.append(int(0))
                        image_front_id.append(int(0))

                    if image_back is not None:
                        # use back_image
                        image_back_id.append(int(1))
                        image_back_id.append(int(1))
                        image_back_id.append(int(1))
                    else:
                        # otherwise default color
                        image_back_id.append(int(0))
                        image_back_id.append(int(0))
                        image_back_id.append(int(0))

                line_obj_file = obj_file.readline()

        # if image_front is specified then ignore mtl file // image_back can still be manually specified -> doesn't exist atm via mtl file
        if image_front is not None:
            image_front_array = [image_front]
        elif material_library is not None:
            with open(material_library) as mtl_file:
                line_mtl_file = mtl_file.readline()
                while line_mtl_file:
                    if line_mtl_file[:6] == "map_Kd":
                        # store texture name .mtl
                        line_mtl_file.split(" ")
                        # fix the \n crap instead of :-1
                        image_front_array.append(line_mtl_file[7:-1])
                    line_mtl_file = mtl_file.readline()

        return vertices, triangles, uvs, uvs_ind, normals, normal_ind, image_front_id, image_back_id, image_front_array, image_back
