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

        path_finder = ShortestPathFinder(vertices, triangles, triangle_weights=triangle_weights)

        self.assertAlmostEqual(sqrt(2), path_finder.get_path_cost(start, end))

        path_finder = ShortestPathFinder(vertices, triangles, triangle_weights=triangle_weights[::-1])

        self.assertAlmostEqual(sqrt(2), path_finder.get_path_cost(start, end))


class TestExactShortestPathInSquare(TestCase):
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


class TestShortestPathInSquareWithSubdivisions(TestCase):
    def setUp(self):
        self.vertices = [(0, 0),
                         (0, 1),
                         (1, 1),
                         (1, 0)]

        self.triangles = [(0, 1, 3),
                          (1, 2, 3)]

        self.path_finder = ShortestPathFinder(self.vertices, self.triangles)

    def test_acrossOppositeDiagonal(self):
        cost, path = self.path_finder.shortest_path((0, 0), (1, 1), subdivisions=4)

        self.assertAlmostEqual(sqrt(2), cost)

    def test_shortenedPathAcrossOppositeDiagonal(self):
        cost, path = self.path_finder.shortest_path((1 / 4, 1 / 4),
                                                    (3 / 4, 3 / 4),
                                                    subdivisions=2)
        self.assertAlmostEqual(sqrt(2) / 2, cost)


class TestShortestPathWithDifferentWeights(TestCase):
    def setUp(self):
        self.vertices = [(0, 0),
                         (1 / 2, 0),
                         (1, 0),
                         (1 / 2, 1 / 2),
                         (0, 1),
                         (1 / 2, 1),
                         (1, 1)]

        self.triangles = [(0, 3, 1),
                          (0, 4, 3),
                          (3, 4, 5),
                          (3, 5, 6),
                          (3, 6, 2),
                          (1, 3, 2)]

        self.triangle_weights = [1, 1, 1, 2, 2, 2]

        self.path_finder = ShortestPathFinder(self.vertices, self.triangles, triangle_weights=self.triangle_weights)

    def test_unBendingShortestPathsAcrossBoundary(self):
        s, e = ((0, 1 / 2), (1, 1 / 2))

        for subdivisions in range(1, 3):
            cost, path = self.path_finder.shortest_path(s, e, subdivisions=subdivisions)
            self.assertAlmostEqual(1.5, cost,
                                   msg='Shortest path between {0!s} and {1!s} with {2!s} subdivisions had cost: {3!s}'.format(
                                       s, e, subdivisions, cost))


    def test_unBendingShortestPathAlongBoundary(self):
        s, e = ((1 / 2, 0), (1 / 2, 1))

        for subdivisions in range(1, 3):
            cost, path = self.path_finder.shortest_path(s, e, subdivisions=subdivisions)
            self.assertAlmostEqual(1, cost,
                                   msg='Shortest path between {0!s} and {1!s} with {2!s} subdivisions had cost: {3!s}'.format(
                                       s,
                                       e,
                                       subdivisions,
                                       cost))
