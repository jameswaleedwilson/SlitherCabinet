import numpy as np
from math import *


class TransformationMatrices:
    def __init__(self, angle, axis):
        self.angle = angle
        self.axis = axis


def orthographic_mat(aspect_ratio, near_plane, far_plane, zoom):
    max_x = max(fabs(-zoom), fabs(zoom))
    # print(max_x)
    max_y = max(fabs(-zoom), fabs(zoom))
    # print(max_y)
    greater_xy = max(max_x, max_y)
    screen_right = greater_xy * aspect_ratio
    screen_top = greater_xy
    screen_left = -screen_right
    screen_bottom = -screen_top
    near_plane = near_plane
    far_plane = far_plane
    # ortho LH
    return np.array([[1 / (screen_right - screen_left), 0, 0, -((screen_right + screen_left) / (screen_right -
                                                                                                screen_left))],
                     [0, 1 / (screen_top - screen_bottom), 0, -((screen_top + screen_bottom) / (screen_top -
                                                                                                screen_bottom))],
                     [0, 0, 1 / (far_plane - near_plane), -((far_plane + near_plane) / (far_plane - near_plane))],
                     [0, 0, 0, 1]], np.float32)


def identity_mat():
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], np.float32)


def translate_mat(x, y, z):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]], np.float32)


def scale_mat(s):
    return np.array([[s, 0, 0, 0],
                     [0, s, 0, 0],
                     [0, 0, s, 0],
                     [0, 0, 0, 1]], np.float32)


def scale_mat3(sx, sy, sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_x_mat(angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_y_mat(angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_z_mat(angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_axis(angle, axis):
    c = cos(radians(angle))
    s = sin(radians(angle))
    axis = axis.normalize()
    ux2 = axis.x*axis.x
    uy2 = axis.y*axis.y
    uz2 = axis.z*axis.z
    return np.array([[c + (1-c)*ux2, (1-c)*axis.y*axis.x - s*axis.z, (1-c)*axis.z*axis.x + s*axis.y, 0],
                     [(1-c)*axis.y*axis.x + s*axis.z, c+(1-c)*uy2, (1-c)*axis.z*axis.y - s*axis.x, 0],
                     [(1-c)*axis.x*axis.z - s*axis.y, (1-c)*axis.y*axis.z + s*axis.x, c+(1-c)*uz2, 0],
                     [0, 0, 0, 1]], np.float32)


def translate(matrix, x, y, z):
    trans = translate_mat(x, y, z)
    return matrix @ trans


def scale(matrix, s):
    sc = scale_mat(s)
    return matrix @ sc


def scale3(matrix, x, y, z):
    sc = scale_mat3(x, y, z)
    return matrix @ sc


def rotate(matrix, angle, axis, local=True):
    rot = identity_mat()
    if axis == "x":
        rot = rotate_x_mat(angle)
    if axis == "y":
        rot = rotate_y_mat(angle)
    if axis == "z":
        rot = rotate_z_mat(angle)
    if local:
        # print('local', matrix @ rot)
        return matrix @ rot
    else:
        # print('global', rot @ matrix)
        return rot @ matrix


def rotate_a(matrix, angle, axis, local=True):
    rot = rotate_axis(angle, axis)
    if local:
        return matrix @ rot
    else:
        return rot @ matrix
