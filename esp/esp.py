from math import sqrt

import numpy as np
import matplotlib.tri as tri

from esp.dijkstra import dijkstra


class ShortestPathFinder(object):
    def __init__(self, vertices, triangles, triangle_weights=None):
        self.vertices = vertices
        self.triangles = triangles
        self.triangle_weights = triangle_weights or [1 for _ in triangles]
        self.triangulation = tri.Triangulation([v[0] for v in vertices],
                                               [v[1] for v in vertices],
                                               triangles=triangles)

        self.tri_finder = self.triangulation.get_trifinder()

    def get_path_cost(self, start, end):
        """
        Get cost of path.

        Start and end points are assumed (by construction) to be on edge
        or vertices of a triangle.

        :param start:
        :param end:
        :return:
        """
        s, e = start, end
        dx = e[0] - s[0]
        dy = e[1] - s[1]
        m = dy/dx

        x0 = s[0] + 1 / 2 * (dx)
        y0 = s[1] + 1 / 2 * (dy)
        path_mid_point = (x0,
                          y0)

        p = path_mid_point

        y_perp = lambda x: -1/m*x+(y0-x0/m)

        eps = 1e-8
        point1 = (p[0] + eps, p[1] + eps * y_perp(eps))
        point2 = (p[0] - eps, p[1] - eps * y_perp(eps))

        triangle1 = self.tri_finder(*point1)
        triangle2 = self.tri_finder(*point2)

        min_tri_weight = min(self.triangle_weights[triangle1],
                             self.triangle_weights[triangle2])

        path_length = sqrt((s[0] - e[0]) ** 2 + (s[1] - e[1]) ** 2)
        return path_length * min_tri_weight

    def _base_triangulation_coordinates(self):
        return [(x, y) for x, y in zip(self.triangulation.x, self.triangulation.y)]

    def _create_graph(self, triangulation):
        graph = []

        coordinates = [(x, y) for x, y in zip(triangulation.x, triangulation.y)]

        for edge in triangulation.edges:
            graph.append((edge[0], edge[1], self.get_path_cost(coordinates[edge[0]],
                                                               coordinates[edge[1]])))
        return graph

    def shortest_path(self, start=None, end=None):

        vertices = self._base_triangulation_coordinates()

        if start not in vertices:
            vertices.append(start)

        if end not in vertices:
            vertices.append(end)

        triangulation = tri.Triangulation([v[0] for v in vertices],
                                          [v[1] for v in vertices])

        coordinates = [(x, y) for x, y in zip(triangulation.x, triangulation.y)]

        v1_index = coordinates.index(start)
        v2_index = coordinates.index(end)

        cost, path = dijkstra(self._create_graph(triangulation),
                              v1_index,
                              v2_index)

        return cost, tuple(coordinates[idx] for idx in path)
