import numpy as np
from munkres import Munkres

def prepareMatrix(m: np.ndarray) -> np.ndarray:
    """
    Prepares the matrix by padding it with zeros if it is not square.

    Args:
        m (np.ndarray): The input matrix.

    Returns:
        np.ndarray: The padded square matrix.
    """
    if m.shape[0] == m.shape[1]:
        return m
    padded = np.zeros((max(m.shape), max(m.shape)), dtype=int)
    padded[:m.shape[0], :m.shape[1]] = m
    return padded

def hungarian(m: np.ndarray) -> list[tuple[int, int]]:
    """
    Solves the assignment problem using the Hungarian algorithm.

    Args:
        m (np.ndarray): The input cost matrix.
        
    Returns:
        list of tuples: A list of tuples where each tuple represents 
                an assignment (row, column) that minimizes the total cost.
    """
    m = prepareMatrix(m)
    munkers = Munkres()
    cost = m.max() - m
    indexes = munkers.compute(cost)
    return indexes