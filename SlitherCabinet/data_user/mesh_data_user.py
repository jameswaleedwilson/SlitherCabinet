import pygame

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
material_3 = {"name": "Laminex_Sepia_Walnut_AbsoluteGrain",
              "manufacturer_colour_code": 2614,
              "double_sided": False,
              "image_face": "laminex_sepia_walnut_absoluteGrain.jpg", #image face
              "image_reverse": "light_jarrah_truescale_absoluteGrain.jpg",
              "image_substrate": "medium_density_fiberboard.jpg",
              "finish": "stipple",
              "nominal_thickness": 16,
              "actual_thickness": 16.3,
              "sheet_size": "2400x1200",
              "edge_thickness": 1
              }

# cabinet
cabinet_width = 600
cabinet_depth = 560
cabinet_height = 720
kick_height = 100
rail_depth = 100

left_gable_material = material_3
right_gable_material = material_3
back_material = material_3
base_material = material_3
rail_material = material_3



mesh_data_user = \
    [

        {
            "part": "right_gable",
            "mesh": "meshesOBJ/floor_right_gable_parametric.obj",
            "image_face_array": {"image_face": right_gable_material["image_face"],
                                 "image_reverse": right_gable_material["image_reverse"],
                                 "image_substrate": right_gable_material["image_substrate"]
                                 },
            "identifier": (1, 0, 0),
            "location": (100, 0, 0),
            "rotation": (0, pygame.Vector3(0, 1, 0)),
            "variables": {"cabinet_width": cabinet_width, "cabinet_depth": cabinet_depth, "cabinet_height": cabinet_height,
                          "right_gable_thickness": right_gable_material["actual_thickness"],
                          "right_gable_edge_thickness": right_gable_material["edge_thickness"],
                          "left_gable_thickness": left_gable_material["actual_thickness"],
                          "back_thickness": back_material["actual_thickness"],
                          "base_thickness": base_material["actual_thickness"],
                          "rail_thickness": rail_material["actual_thickness"],
                          "rail_depth": rail_depth
                          }
        },

    ]