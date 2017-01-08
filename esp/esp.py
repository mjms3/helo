from math import sqrt
import decimal

decimal.getcontext().prec = 8
import itertools
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from decimal import Decimal

from esp.dijkstra import dijkstra


class ShortestPathFinder(object):
    def __init__(self, vertices, triangles, triangle_weights=None):
        self.vertices = [(Decimal(v[0]), Decimal(v[1])) for v in vertices]
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

        x0 = s[0] + 1 / 2 * (dx)
        y0 = s[1] + 1 / 2 * (dy)
        path_mid_point = (x0,
                          y0)

        p = path_mid_point

        eps = 5e-8
        if abs(dy) < eps:
            point1 = (p[0] + eps, p[1])
            point2 = (p[0] - eps, p[1])
        elif abs(dx) < eps:
            point1 = (p[0], p[1] + eps)
            point2 = (p[0], p[1] - eps)
        else:
            m = dy / dx
            y_perp = lambda x: -1 / m * x + (y0 - x0 / m)

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

    def _create_graph(self, triangulation, subdivisions=1):
        graph = []

        coordinates = [(x, y) for x, y in zip(triangulation.x, triangulation.y)]
        for triangle in triangulation.triangles:

            new_points = []
            for idx in range(3):
                v1_idx = triangle[idx]
                v2_idx = triangle[(idx + 1) % 3]
                p1 = (coordinates[v1_idx][0], coordinates[v1_idx][1])
                p2 = (coordinates[v2_idx][0], coordinates[v2_idx][1])
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                for i_sub in range(subdivisions + 1):
                    x_prime = p1[0] + i_sub / subdivisions * dx
                    y_prime = p1[1] + i_sub / subdivisions * dy
                    new_points.append((x_prime, y_prime))

            for edge in itertools.product(new_points, repeat=2):

                if edge[0] != edge[1]:
                    graph.append((edge[0], edge[1], self.get_path_cost(edge[0], edge[1])))
        return list(set(graph))

    def shortest_path(self, start=None, end=None, subdivisions=1):
        start_dec = (Decimal(start[0]), Decimal(start[1]))
        end_dec = (Decimal(end[0]), Decimal(end[1]))

        triangulation = self._get_new_triangulation(start, end)

        cost, path = dijkstra(self._create_graph(triangulation, subdivisions=subdivisions),
                              start_dec, end_dec)

        return cost, path

    def _get_new_triangulation(self, start, end):

        vertices = self._base_triangulation_coordinates()

        if start not in vertices:
            vertices.append(start)
        if end not in vertices:
            vertices.append(end)

        x_coordinates = [v[0] for v in vertices]
        y_coordinates = [v[1] for v in vertices]
        triangulation = tri.Triangulation(x_coordinates,
                                          y_coordinates)

        return triangulation

    def plot_shortest_path(self, start, end, subdivisions=1):
        graph = self._create_graph(self.triangulation, subdivisions=subdivisions)
        cost, path = self.shortest_path(start, end, subdivisions)

        plt.figure()
        plt.gca().set_aspect('equal')
        for edge in graph:
            p1 = edge[0]
            p2 = edge[1]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'g:',alpha=0.5)
        plt.tripcolor(self.triangulation,self.triangle_weights,cmap=plt.cm.RdYlGn_r)
        plt.plot([p[0] for p in path], [p[1] for p in path], 'k',lw = 3)
        plt.show()
