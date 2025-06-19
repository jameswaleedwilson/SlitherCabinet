import pygame

# cabinet
width = 200
depth = 300
height = 300
# part
# left gable
left_gable_thickness = 16
left_gable_edge_thickness = 1
# right gable
right_gable_thickness = 16
right_gable_edge_thickness = 1
# back
back_thickness = 40
# base
base_thickness = 30
base_edge_thickness = 1
# rail
rail_depth = 100
rail_thickness = 20
rail_edge_thickness = 1


mesh_data_user = \
    [

        {
            "part": "right_gable",
            "mesh": "meshesOBJ/floor_right_gable_parametric.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (6, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (1, 1, 1),
            "dimensions": [width, depth, height,
                           left_gable_thickness, left_gable_edge_thickness,
                           right_gable_thickness, right_gable_edge_thickness,
                           back_thickness, base_thickness, rail_thickness, rail_edge_thickness, base_edge_thickness, rail_depth]
        },

        {
            "part": "right_gable_front_edge",
            "mesh": "meshesOBJ/right_gable_front_edge.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (184, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (1, 1, 1),
            "dimensions": None
        },

        {
            "part": "right_gable_bottom_edge",
            "mesh": "meshesOBJ/right_gable_bottom_edge.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (184, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (1, 1, 1),
            "dimensions": None
        },

        {
            "part": "back",
            "mesh": "meshesOBJ/back.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (left_gable_thickness, depth - back_thickness, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (width - left_gable_thickness - right_gable_thickness,
                      back_thickness,
                      height),
            "dimensions": None
        },

        {
            "part": "base",
            "mesh": "meshesOBJ/floor_base.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (0, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (1, 1, 1),
            "dimensions": None
        },

        {
            "part": "rail",
            "mesh": "meshesOBJ/floor_rail_parametric.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (0, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (1, 1, 1),
            "dimensions": [width, depth, height,
                           left_gable_thickness, left_gable_edge_thickness,
                           right_gable_thickness, right_gable_edge_thickness,
                           back_thickness, base_thickness, rail_thickness, rail_edge_thickness, base_edge_thickness, rail_depth]
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