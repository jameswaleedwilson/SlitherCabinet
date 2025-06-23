string = ("0.000000")


value = eval(string)
formatted_result = f"{value:.6f}"
print(formatted_result)

"""
    {
        "part": "right_gable_front_edge",
        "mesh": "meshesOBJ/right_gable_front_edge.obj",
        "textures": None,
        "identifier": (1, 0, 0),
        "location": (184, 0, 0),
        "rotation": (0, pygame.Vector3(0, 1, 0)),
        "dimensions": None,
        "variables": None
    },

    {
        "part": "right_gable_bottom_edge",
        "mesh": "meshesOBJ/right_gable_bottom_edge.obj",
        "textures": None,
        "identifier": (1, 0, 0),
        "location": (184, 0, 0),
        "rotation": (0, pygame.Vector3(0, 1, 0)),
        "dimensions": None,
        "variables": None
    },

    {
        "part": "back",
        "mesh": "meshesOBJ/floor_back_parametric.obj",
        "textures": None,
        "identifier": (1, 0, 0),
        "location": (0, 100, 0),
        "rotation": (0, pygame.Vector3(0, 1, 0)),
        "variables": {"width": width, "depth": depth, "height": height,
                      "back_thickness": back_thickness,
                      "left_gable_thickness": left_gable_thickness, "right_gable_thickness": right_gable_thickness
                      }
    },

    {
        "part": "base",
        "mesh": "meshesOBJ/floor_base_parametric.obj",
        "textures": None,
        "identifier": (1, 0, 0),
        "location": (0, 0, 0),
        "rotation": (0, pygame.Vector3(0,1,0)),
        "variables": {"width": width, "depth": depth,
                      "base_thickness": base_thickness, "base_edge_thickness": base_edge_thickness,
                      "left_gable_thickness": left_gable_thickness, "right_gable_thickness": right_gable_thickness, "back_thickness": back_thickness
                      }
    },

    {
        "part": "rail",
        "mesh": "meshesOBJ/floor_rail_parametric.obj",
        "textures": None,
        "identifier": (1, 0, 0),
        "location": (0, 0, 0),
        "rotation": (0, pygame.Vector3(0,1,0)),
        "variables": {"width": width, "height": height,
                      "rail_depth": rail_depth, "rail_thickness": rail_thickness, "rail_edge_thickness": rail_edge_thickness,
                      "left_gable_thickness": left_gable_thickness, "right_gable_thickness": right_gable_thickness
                      }
    },
"""