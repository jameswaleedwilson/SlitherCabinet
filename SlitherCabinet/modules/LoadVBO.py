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
                 # images -> covert to texture in load_texture
                 image_face_array=None,  #image textures from obj
                 image_face=None,
                 # back face of triangle not 3D object not seen if image culling is True
                 image_back=None,
                 # draw type
                 draw_type=GL_TRIANGLES,
                 # local once off change
                 location=pygame.Vector3(0, 0, 0),
                 rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 std_scale=pygame.Vector3(1, 1, 1),
                 # animation
                 move_rotation=TransformationMatrices(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),
                 # shader program
                 shader=None,
                 # parametric .obj variables
                 variables=None,
                 # identifying RGB for pixel picking (0-255, 0-255, 0-255)
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
         image_back) = self.load_mesh(obj_filename, image_face, image_back, variables, image_face_array)

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
    def load_mesh(filename, image_face, image_back, variables=None, image_face_array=None):
        vertices = []
        triangles = []
        normals = []
        # normal_indices
        normal_ind = []
        uvs = []
        # uvs_indices
        uvs_ind = []
        # https://www.khronos.org/opengl/wiki/Array_Texture upgrade multiple textures to arrays ????
        mtl_library = None
        image_front_id = 0
        image_front_array_id = []
        image_front_array = []
        # this is the backside of a face not 3D object, currently single element
        image_back_id = []


        with open(filename) as obj_file:
            line_obj_file = obj_file.readline()
            while line_obj_file:

                if line_obj_file[:6] == "mtllib":
                    # store material library name .mtl
                    mtl_library = "meshesOBJ/" + line_obj_file[7:-1]

                if line_obj_file[:2] == "v ":
                    vx, vy, vz = [value for value in line_obj_file[2:].split()]
                    if variables is not None:
                        vx = value_from_string_formula(vx, variables)
                        vy = value_from_string_formula(vy, variables)
                        vz = value_from_string_formula(vz, variables)

                    vx, vy, vz = float(vx), float(vy), float(vz)

                    vertices.append((vx, vy, vz))

                if line_obj_file[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line_obj_file[3:].split()]
                    normals.append((vx, vy, vz))

                if line_obj_file[:2] == "vt":
                    vx, vy = [float(value) for value in line_obj_file[2:].split()]
                    uvs.append((vx, vy))

                # counts images from 1, 0 = default
                if line_obj_file[:6] == "usemtl":
                    image_front_id += 1

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

                    # use front_image first
                    if image_face is not None:
                        image_front_array_id.append(int(1))
                        image_front_array_id.append(int(1))
                        image_front_array_id.append(int(1))
                    elif mtl_library is not None:
                        # image_front does not exist try .obj file usemtl...
                        image_front_array_id.append(int(image_front_id))
                        image_front_array_id.append(int(image_front_id))
                        image_front_array_id.append(int(image_front_id))
                    else:
                        # otherwise default to a solid color defined in LoadVBO
                        image_front_array_id.append(int(0))
                        image_front_array_id.append(int(0))
                        image_front_array_id.append(int(0))

                    # this is the backside of a face not 3D object
                    if image_back is not None:
                        # use back_image 1 = True
                        image_back_id.append(int(1))
                        image_back_id.append(int(1))
                        image_back_id.append(int(1))
                    else:
                        # use back_image 0 = False, otherwise default color???
                        image_back_id.append(int(0))
                        image_back_id.append(int(0))
                        image_back_id.append(int(0))

                line_obj_file = obj_file.readline()

        # if image_front is specified then ignore mtl file // image_back can still be manually specified -> doesn't exist atm via mtl file
        # consider ignoring the mtl file altogether as values will be stored with materials
        if image_face is not None:
            image_front_array = [image_face]
        elif mtl_library is not None:
            with open(mtl_library) as mtl_file:
                line_mtl_file = mtl_file.readline()
                while line_mtl_file:
                    if line_mtl_file[:6] == "map_Kd":
                        # store texture name .mtl
                        line_mtl_file.split(" ")

                        if image_face_array is not None:
                            # fix the \n crap instead of :-1 + 4 to remove.jpg
                            texture = line_mtl_file[7:-5]
                            texture = find_image_from_material(texture, image_face_array)
                            image_front_array.append(str("images/" + texture))
                        # need to add check here to use mtl file if images are not supplied for example on static colored products
                        else:
                            image_front_array.append(str("images/debug_empty.png"))
                    line_mtl_file = mtl_file.readline()

        return vertices, triangles, uvs, uvs_ind, normals, normal_ind, image_front_array_id, image_back_id, image_front_array, image_back
