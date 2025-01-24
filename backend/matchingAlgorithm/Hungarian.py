import numpy as np
from munkres import Munkres

def prepareMatrix(m):
    if m.shape[0] == m.shape[1]:
        return m
    padded = np.zeros((max(m.shape), max(m.shape)), dtype=int)
    padded[:m.shape[0], :m.shape[1]] = m
    return padded

def hungarian(m):
    m = prepareMatrix(m)
    munkers = Munkres()
    cost = m.max() - m
    indexes = munkers.compute(cost)
    total = 0
    print(m)
    for row, column in indexes:
        value = m[row][column]
        total += value
        print(f'({row}, {column}) -> {value}')
    print(f'total weight: {total}')
    
m = np.array([
    [0, 0, 6, 9, 0],
    [0, 6, 1, 0, 0],
    [0, 1, 2, 0, 0],
    [8, 7, 0 ,3, 5],
    [6, 0, 0, 0, 3],
])
hungarian(m)