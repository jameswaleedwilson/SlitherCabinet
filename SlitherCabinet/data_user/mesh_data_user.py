import pygame

# cabinet
width = 600
depth = 560
height = 720
# materials
material_1 = {"double_sided": True,
           "color": "laminex_midnight_oak_truescale", # image = sdfjhasgfkjhs.jpg
           "finish": "natural",
           "substrate": "particle_board"
              }
material_2 = {"double_sided": True,
           "color": "laminex_sepia_walnut_absoluteGrain",
           "finish": "absolute_grain",
           "substrate": "particle_board"
              }
material_3 = {"double_sided": False,
           "color_face": "laminex_sepia_walnut_absoluteGrain",
           "color_reverse": "light_jarrah_truescale_absoluteGrain",
           "finish": "stipple",
           "substrate": "medium_density_fiberboard",
           "nominal_thickness": 16,
           "actual_thickness": 16.3,
           "sheet_size": "2400x1200",
           "edge_thickness": 1
              }

# part
# left gable
left_gable_thickness = 16
left_gable_edge_thickness = 1
# right gable
right_gable_material = material_3
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
            "textures": material_3, # only include the 3 textures
            "identifier": (1, 0, 0),
            "location": (100, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "variables": {"width": width, "depth": depth, "height": height,
                          "right_gable_thickness": right_gable_material["actual_thickness"], "right_gable_edge_thickness": right_gable_material["edge_thickness"],
                          "left_gable_thickness": left_gable_thickness, "base_thickness": base_thickness,
                          "back_thickness": back_thickness, "rail_thickness": rail_thickness, "rail_depth": rail_depth
                          }
        },

    ]