import numpy as np

def triangulation_to_graph(triangulation):
    graph = []
    for edge in triangulation.edges:
        v1,v2 = edge
        xdiff = triangulation.x[v1]-triangulation.x[v2]
        ydiff = triangulation.y[v1]-triangulation.y[v2]
        norm = np.sqrt(xdiff**2+ydiff**2)
        graph.append((edge[0], edge[1], norm))
    return graph