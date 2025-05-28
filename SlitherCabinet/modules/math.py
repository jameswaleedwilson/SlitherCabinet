import math


def subtract(v0, v1):
    return [v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2]]


def dot(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]


def length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def normalize(v):
    length2 = length(v)
    return [v[0] / length2, v[1] / length2, v[2] / length2]


def multi(v, s):
    return [v[0] * s, v[1] * s, v[2] * s]


def add(v0, v1):
    return [v0[0] + v1[0], v0[1] + v1[1], v0[2] + v1[2]]


def cross(v0, v1):
    return [
        v0[1] * v1[2] - v1[1] * v0[2],
        v0[2] * v1[0] - v1[2] * v0[0],
        v0[0] * v1[1] - v1[0] * v0[1]]