from collections import defaultdict
from heapq import *


def flatten_path(path):
    path_list = []
    curr_elt, next_elt = path
    while next_elt:
        path_list.append(curr_elt)
        curr_elt,next_elt = next_elt
    path_list.append(curr_elt)
    return tuple(path_list[::-1])

def dijkstra(graph, start_vertex, end_vertex):
    """From: https://gist.github.com/kachayev/5990802

    :param graph:
    :param start_vertex:
    :param end_vertex:
    :return:
    """

    # Make the graph undirected
    graph += [(elt[1],elt[0],elt[2]) for elt in graph]

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
                return (cost, flatten_path(path))

            for weight, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost + weight, v2, path))

    return float("inf")


if __name__ == "__main__":
    edges = [
        ("A", "B", 7),
        ("A", "D", 5),
        ("B", "C", 8),
        ("B", "D", 9),
        ("B", "E", 7),
        ("C", "E", 5),
        ("D", "E", 15),
        ("D", "F", 6),
        ("E", "F", 8),
        ("E", "G", 9),
        ("F", "G", 11)
    ]

    print("=== Dijkstra ===")
    print(edges)
    print("A -> E:")
    print(dijkstra(edges, "A", "E"))
    print("F -> G:")
    print(dijkstra(edges, "F", "G"))
