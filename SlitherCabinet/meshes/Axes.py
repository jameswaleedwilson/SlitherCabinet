from SlitherCabinet.modules.LoadDefaultFBO import LoadDefaultFBO


class Axes(LoadDefaultFBO):
    def __init__(self, location, shader):
        vertices = [[0.0, 0.0, 0.0],
                    [600.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0],
                    [0.0, 300.0, 0.0],
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 50.0]]

        colors = [[1.0, 0.0, 0.0],
                  [1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0],
                  [0.0, 1.0, 0.0],
                  [0.0, 0.0, 1.0],
                  [0.0, 0.0, 1.0]]
        super().__init__(vertices,
                         vertex_colors=colors,
                         draw_type=GL_LINES,
                         translation=location,
                         shader=shader)
