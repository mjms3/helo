from esp.esp import ShortestPathFinder

vertices = [(0, 0),
            (1 / 2, 0),
            (1, 0),
            (1 / 2, 1 / 2),
            (0, 1),
            (1 / 2, 1),
            (1, 1)]

triangles = [(0, 3, 1),
             (0, 4, 3),
             (3, 4, 5),
             (3, 5, 6),
             (3, 6, 2),
             (1, 3, 2)]

path_finder = ShortestPathFinder(vertices, triangles, triangle_weights=[1, 1, 1, 2, 2, 2])

path_finder.plot_shortest_path((0, 0), (1, 1), subdivisions=8)
