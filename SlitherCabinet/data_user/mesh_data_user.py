import pygame

mesh_data_user = \
    [
        {
            "part": "left gable",
            "mesh": "meshesOBJ/cube.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (0, 0, -16),
            "rotation": (-90, pygame.Vector3(0,1,0)),
            "scale": (100, 100, 16)
        },

        {
            "part": "base",
            "mesh": "meshesOBJ/cube.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (16, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (68, 84, 16)
        },

        {
            "part": "back",
            "mesh": "meshesOBJ/cube.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (16, 84, 0),
            "rotation": (-90, pygame.Vector3(0,1,0)),
            "scale": (100, 84, 16)
        },

        {
            "part": "rail",
            "mesh": "meshesOBJ/cube.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (16, 0, 84),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (68, 50, 16)
        },

        {
            "part": "right gable",
            "mesh": "meshesOBJ/cube.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (0, 0, -100),
            "rotation": (-90, pygame.Vector3(0,1,0)),
            "scale": (100, 100, 16)
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