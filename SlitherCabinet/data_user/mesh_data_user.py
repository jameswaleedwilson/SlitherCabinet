import pygame

width = 200
depth = 100
height = 150
material_1_thickness = 16
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
            "scale": (1, 1, 1),
            "dimensions": [material_1_thickness, depth, height]
        },

        {
            "part": "right gable",
            "mesh": "meshesOBJ/right_gable.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (width - material_1_thickness, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (material_1_thickness, depth, height),
            "dimensions": None
        },

        {
            "part": "back",
            "mesh": "meshesOBJ/back.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (material_1_thickness, depth - material_1_thickness, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (width - 2 * material_1_thickness, material_1_thickness, height),
            "dimensions": None
        },

        {
            "part": "base",
            "mesh": "meshesOBJ/base.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (material_1_thickness, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (width - 2 * material_1_thickness, depth - material_1_thickness, material_1_thickness),
            "dimensions": None
        },

        {
            "part": "rail",
            "mesh": "meshesOBJ/rail.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (material_1_thickness, 0, height - material_1_thickness),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (width - 2 * material_1_thickness, rail_depth, material_1_thickness),
            "dimensions": None
        },

        {
            "part": "hinge",
            "mesh": "meshesOBJ/hinge.obj",
            "texture_front": "textures/dark_grey.png",
            "identifier": (1, 0, 0),
            "location": (84, 40, 50),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (1000, 1000, 1000),
            "dimensions": None
        },
    ]