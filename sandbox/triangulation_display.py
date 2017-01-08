
from esp.esp import ShortestPathFinder

vertices = [(0, 0),
            (0, 1),
            (1, 1),
            (1, 0)]

triangles = [(0, 1, 3),
             (1, 2, 3)]

path_finder = ShortestPathFinder(vertices, triangles)

path_finder.plot_shortest_path((1/4,1/4),(3/4,3/4),subdivisions=2)