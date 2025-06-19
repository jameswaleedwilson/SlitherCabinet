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

def formula_from_string(string, obj_dimensions):
    width = obj_dimensions[0]
    depth = obj_dimensions[1]
    height = obj_dimensions[2]
    left_gable_thickness = obj_dimensions[3]
    left_gable_edge_thickness = obj_dimensions[4]
    right_gable_thickness = obj_dimensions[5]
    right_gable_edge_thickness = obj_dimensions[6]
    back_thickness = obj_dimensions[7]
    base_thickness = obj_dimensions[8]
    rail_thickness = obj_dimensions[9]
    rail_edge_thickness = obj_dimensions[10]
    base_edge_thickness = obj_dimensions[11]
    rail_depth = obj_dimensions[12]
    value = eval(string)
    formatted_result = f"{value:.6f}"
    return formatted_result
