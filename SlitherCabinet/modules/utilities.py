from OpenGL.GL import *
import numpy as np


def format_vertices(coordinates, triangles):
    all_triangles = []
    for t in range(0, len(triangles), 3):
        all_triangles.append(coordinates[triangles[t]])
        all_triangles.append(coordinates[triangles[t + 1]])
        all_triangles.append(coordinates[triangles[t + 2]])
    return np.array(all_triangles, np.float32)


def compile_shader(shader_type, shader_source):
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, shader_source)
    glCompileShader(shader_id)
    compile_success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not compile_success:
        error_message = glGetShaderInfoLog(shader_id)
        glDeleteShader(shader_id)
        error_message = "\n" + error_message.decode("utf-8")
        raise Exception(error_message)
    return shader_id


def link_shader(vertex_shader_code, fragment_shader_code):
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader_code)
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_code)
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)
    link_success = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not link_success:
        info = glGetShaderInfoLog(program_id)
        raise RuntimeError(info)
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)
    return program_id

def value_from_string_formula(string_formula, variables):
    value = eval(string_formula, variables)
    formatted_result = f"{value:.6f}"
    return formatted_result

def find_image_from_material(string, image_face_array):
    image = eval(string, image_face_array)
    formatted_result = str(image)
    return formatted_result

# old function for iterating through nested dict
def find_texture2(string, textures):
    for key, value in textures.items():
        if string == key:
            formatted_result = value + ".jpg"
            return formatted_result
