import pygame

width = 100
depth = 100
height = 100
cth = 16
rail_depth = 50

mesh_data_user = \
    [
        {
            "part": "left gable",
            "mesh": "meshesOBJ/left_gable.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (0, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (cth, depth, height)
        },

        {
            "part": "base",
            "mesh": "meshesOBJ/base.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (cth, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (width - 2 * cth, depth - cth, cth)
        },

        {
            "part": "back",
            "mesh": "meshesOBJ/back.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (cth, depth - cth, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (width - 2 * cth, cth, height)
        },

        {
            "part": "rail",
            "mesh": "meshesOBJ/rail.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (cth, 0, height - cth),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (width - 2 * cth, rail_depth, cth)
        },

        {
            "part": "right gable",
            "mesh": "meshesOBJ/right_gable.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (width - cth, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (cth, depth, height)
        },

        {
            "part": "hinge",
            "mesh": "meshesOBJ/hinge.obj",
            "texture_front": "textures/dark_grey.png",
            "identifier": (1, 0, 0),
            "location": (84, 40, 50),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (1000, 1000, 1000)
        },
    ]