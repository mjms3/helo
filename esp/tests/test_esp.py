from math import sqrt
from unittest import TestCase
import matplotlib.tri as tri
import numpy as np

from esp.dijkstra import dijkstra
from esp.esp import triangulation_to_graph


class TestShortestPathInSquare(TestCase):
    def setUp(self):
        self.vertices = np.asarray([[0, 0],
                                    [1, 0],
                                    [0, 1],
                                    [1, 1],
                                    [1 / 2, 1 / 2]], dtype=np.float64)

        self.edges = np.asarray([[0, 2, 4],
                                 [0, 4, 1],
                                 [1, 4, 3],
                                 [4, 2, 3]],dtype=np.int)

        self.triangulation = tri.Triangulation(self.vertices[:, 0],
                                               self.vertices[:, 1],
                                               triangles=self.edges)


    def test_shortestPathAlongEdges_isCornerToCorner(self):
        graph = triangulation_to_graph(self.triangulation)
        cost, path = dijkstra(graph,0,3)
        self.assertAlmostEqual(sqrt(2),cost)
        self.assertEqual((0,4,3),path)
