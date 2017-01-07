from collections import defaultdict
from heapq import *


def flatten_path(path):
    path_list = []
    curr_elt, next_elt = path
    while next_elt:
        path_list.append(curr_elt)
        curr_elt, next_elt = next_elt
    path_list.append(curr_elt)
    return tuple(path_list[::-1])


def dijkstra(graph, start_vertex, end_vertex):
    """From: https://gist.github.com/kachayev/5990802

    :param graph:
    :param start_vertex:
    :param end_vertex:
    :return:
    """

    g = defaultdict(list)
    for vertex1, vertex2, weight in graph:
        g[vertex1].append((weight, vertex2))

    q, seen = [(0, start_vertex, ())], set()
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == end_vertex:
                return cost, flatten_path(path)

            for weight, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost + weight, v2, path))

    return float("inf")
