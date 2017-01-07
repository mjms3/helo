import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np



vertices = np.asarray([[0, 0],
                       [1, 0],
                       [0, 1],
                       [1, 1],
                       [1 / 2, 1 / 2]], dtype=np.float64)

edges = np.asarray([[0, 2, 4],
                   [0, 4, 1],
                   [1, 4, 3],
                   [4, 2, 3]])

triangulation = tri.Triangulation(vertices[:,0],vertices[:,1], triangles=edges)

plt.figure()
plt.gca().set_aspect('equal')
plt.triplot(triangulation, 'bo-')
plt.show()
