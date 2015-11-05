import sys
import numpy as np
import time
from optparse import OptionParser
import logging
edges = np.loadtxt('test1.txt')

def normalize(adjacencyMatrix):
    new_matrix=adjacencyMatrix/adjacencyMatrix.sum(axis=0, keepdims=True)
    return new_matrix

def expand(A, E):
    return np.linalg.matrix_power(A, E)

#method for expanding the matrix
def inflate(A, I):
    return normalize(np.power(A, I))


def converge(A):
    pass

def createAdjMatrix(initalMatrix,firstColumn,secondColumn):
    for i in range(firstColumn.size):
        x=firstColumn[i]
        y=secondColumn[i]
        #connecting edges, as it is undirected graph edge is set both ways.
        initalMatrix[x][y]=1.0
        initalMatrix[y][x]=1.0
        #Adding self loops
        initalMatrix[x][x]=1.0
        initalMatrix[y][y]=1.0
    #removing the extra row and column    
    initalMatrix=np.delete(initalMatrix, 0, 0)
    initalMatrix=np.delete(initalMatrix, 0, 1)
    return initalMatrix


def stop(M, i):
    if i%5==4:
        m = np.max( M**2 - M) - np.min( M**2 - M)
        if m==0:
            logging.info("Stop at iteration %s" % i)
            return True
    return False


#taking the max from the array to create new matrix of required dimension
max=np.amax(edges)
print max

#extracting two columns from the original two dimensional array
firstColumn=edges[:,0]
secondColumn=edges[:,1]

#creating the initial empty array, creating one extra dimension to start the index from 1.
initalMatrix=np.ndarray(shape=(max+1,max+1))

#creating the adjacencyMatrix
adjacencyMatrix=createAdjMatrix(initalMatrix,firstColumn,secondColumn)

#normalizing the matrix
matrix=normalize(adjacencyMatrix)

max_loop=10

for i in range(max_loop):
    logging.info("Iteration no", i)
    matrix=expand(matrix,2)
    matrix=inflate(matrix,2)
    if stop(M, i): break
print matrix
