from math import sqrt
from unittest import TestCase

from esp.esp import ShortestPathFinder


class TestGetPathCost(TestCase):
    def test_minimumCostReturnedForPointsOnEdgeIrrespectiveOfOrdering(self):
        vertices = [(0, 0),
                    (0, 1),
                    (1, 1),
                    (1, 0)]

        triangles = [(0, 1, 3),
                     (1, 2, 3)]

        triangle_weights = [1, 2]

        start = (0, 1)
        end = (1, 0)

        pathFinder = ShortestPathFinder(vertices, triangles, triangle_weights=triangle_weights)

        self.assertAlmostEqual(sqrt(2), pathFinder.get_path_cost(start, end))

        pathFinder = ShortestPathFinder(vertices, triangles, triangle_weights=triangle_weights[::-1])

        self.assertAlmostEqual(sqrt(2), pathFinder.get_path_cost(start, end))


class TestShortestPathInSquare(TestCase):
    def setUp(self):
        self.vertices = [(0, 0),
                         (1, 0),
                         (0, 1),
                         (1, 1),
                         (1 / 2, 1 / 2)]

        self.triangles = [[0, 2, 4],
                          [0, 4, 1],
                          [1, 4, 3],
                          [4, 2, 3]]

        self.pathFinder = ShortestPathFinder(self.vertices,
                                             self.triangles)

    def test_shortestPathAlongEdges_isCornerToCorner(self):
        cost, path = self.pathFinder.shortest_path(start=(0, 0),
                                                   end=(1, 1))
        self.assertAlmostEqual(sqrt(2), cost)
        expected_path = ((0, 0),
                         (1 / 2, 1 / 2),
                         (1, 1))
        self.assertEqual(expected_path, path)

    def test_shortestPathAcrossSquare(self):
        cost, path = self.pathFinder.shortest_path(start=(0, 1 / 2),
                                                   end=(1, 1 / 2))
        self.assertAlmostEqual(1, cost)
        expected_path = ((0, 1 / 2),
                         (1 / 2, 1 / 2),
                         (1, 1 / 2))
        self.assertEqual(expected_path, path)

    def test_angledShortestPath(self):
        cost, path = self.pathFinder.shortest_path(start=(0, 1 / 4),
                                                   end=(1, 3 / 4))
        expected_cost = sqrt(1 + 1 / 4)
        expected_path = ((0, 1 / 4),
                         (1 / 2, 1 / 2),
                         (1, 3 / 4))
        self.assertAlmostEqual(expected_cost, cost)
        self.assertEqual(expected_path, path)
