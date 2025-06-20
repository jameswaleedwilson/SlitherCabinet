import pygame

# cabinet
width = 600
depth = 560
height = 720

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
            "variables": {"width": width, "depth": depth, "height": height,
                          "right_gable_thickness": right_gable_thickness, "right_gable_edge_thickness": right_gable_edge_thickness,
                          "left_gable_thickness": left_gable_thickness, "base_thickness": base_thickness,
                          "back_thickness": back_thickness, "rail_thickness": rail_thickness, "rail_depth": rail_depth
                          }
        },

        {
            "part": "right_gable_front_edge",
            "mesh": "meshesOBJ/right_gable_front_edge.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (184, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (1, 1, 1),
            "dimensions": None,
            "variables": None
        },

        {
            "part": "right_gable_bottom_edge",
            "mesh": "meshesOBJ/right_gable_bottom_edge.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (184, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (1, 1, 1),
            "dimensions": None,
            "variables": None
        },

        {
            "part": "back",
            "mesh": "meshesOBJ/floor_back_parametric.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (0, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "scale": (0.25, 0.25, 0.25),
            "variables": {"width": width, "depth": depth, "height": height,
                          "back_thickness": back_thickness,
                          "left_gable_thickness": left_gable_thickness, "right_gable_thickness": right_gable_thickness
                          }
        },

        {
            "part": "base",
            "mesh": "meshesOBJ/floor_base_parametric.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (0, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (1, 1, 1),
            "variables": {"width": width, "depth": depth,
                          "base_thickness": base_thickness, "base_edge_thickness": base_edge_thickness,
                          "left_gable_thickness": left_gable_thickness, "right_gable_thickness": right_gable_thickness, "back_thickness": back_thickness
                          }
        },

        {
            "part": "rail",
            "mesh": "meshesOBJ/floor_rail_parametric.obj",
            "texture_front": None,
            "identifier": (1, 0, 0),
            "location": (0, 0, 0),
            "rotation": (0, pygame.Vector3(0,1,0)),
            "scale": (1, 1, 1),
            "variables": {"width": width, "height": height,
                          "rail_depth": rail_depth, "rail_thickness": rail_thickness, "rail_edge_thickness": rail_edge_thickness,
                          "left_gable_thickness": left_gable_thickness, "right_gable_thickness": right_gable_thickness
                          }
        },

    ]