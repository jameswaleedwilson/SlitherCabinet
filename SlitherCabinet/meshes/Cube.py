from SlitherCabinet.modules.LoadDefaultFBO import LoadDefaultFBO


class Cube(LoadDefaultFBO):
    def __init__(self, location, shader):
        vertices = [[-5, -5, -5],
                    [5, -5, -5],
                    [5, -5, 5],
                    [-5, -5, 5]]

        colors = [[0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0]]
        super().__init__(vertices,
                         vertex_colors=colors,
                         draw_type=GL_LINE_LOOP,
                         translation=location,
                         shader=shader)
