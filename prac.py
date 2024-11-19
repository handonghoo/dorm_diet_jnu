import numpy as np


c = [[0, 1, 2, 0, 0, 0],
     [3, 4, 5, 0, 0, 0],
     [6, 7, 8, 0, 0, 0]]

cc = np.delete(c, (0), axis=0)
print(cc)