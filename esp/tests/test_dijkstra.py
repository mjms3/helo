from math import sqrt
from unittest import TestCase

from esp.dijkstra import dijkstra


class TestDijkstra(TestCase):
    def test_shortestPathBetweenTwoVertices_isTheJoiningEdge(self):
        graph = [(0, 1, 1)]
        cost, path = dijkstra(graph, 0, 1)

        self.assertEqual(1, cost)
        self.assertEqual((0,1), path)

    def test_shortestPathInSquare_isAlongDiagonal(self):
        graph = [(0, 1, 1),
                 (0, 4, sqrt(2) / 2),
                 (1, 4, sqrt(2) / 2),
                 (0, 2, 1),
                 (1, 3, 1),
                 (2, 4, sqrt(2) / 2),
                 (3, 4, sqrt(2) / 2),
                 (2, 3, 1),
                 ]
        cost, path = dijkstra(graph, 0, 3)
        self.assertAlmostEqual(sqrt(2), cost)
        self.assertEqual((0,4,3), path)
