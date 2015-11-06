__author__ = 'hharwani'
import sys
import numpy as np
import logging


#Markov Class
class Markov:

    def normalize(self,adjacencyMatrix):
        adjacencyMatrix = adjacencyMatrix/np.sum(adjacencyMatrix,axis = 0)
        return adjacencyMatrix

    #method for expanding the matrix
    def expand(self,A, M):
        return np.linalg.matrix_power(A,M)

    #method for inflating the matrix
    def inflate(self,A, R):
        return self.normalize(np.power(A,R))

    #method for getting the clusters
    def get_clusters(self,A):
        clusters = []
        for i, r in enumerate((A>0).tolist()):
            if r[i]:
                clusters.append(A[i,:]>0)
        clust_map  ={}
        for cn , c in enumerate(clusters):
            for x in  [ i for i, x in enumerate(c) if x ]:
                clust_map[cn] = clust_map.get(cn, [])  + [x]
        return clust_map


#Utility class
class Util:
    def createAdjMatrix(Self,initalMatrix,firstColumn,secondColumn):
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

def main():
    files=["new_att.txt","new_collaboration.txt","new_yeast.txt"]
    for file in files:
        print "For file-->",file
        edges = np.loadtxt(file)
        #taking the max from the array to create new matrix of required dimension
        max=np.amax(edges)
        print max

        #extracting two columns from the original two dimensional array
        firstColumn=edges[:,0]
        secondColumn=edges[:,1]

        #creating the initial empty array, creating one extra dimension to start the index from 1.
        initalMatrix=np.ndarray(shape=(max+1,max+1))

        #creating the adjacencyMatrix
        adjacencyMatrix=Util().createAdjMatrix(initalMatrix,firstColumn,secondColumn)

        #normalizing the matrix
        matrix=Markov().normalize(adjacencyMatrix)

        max_loop=1000
        r=2.0
        m=2
        for i in range(max_loop):
            print("Iteration no-->,", i)
            #maintaining a previous copy for checking convergence
            prev = matrix.copy();
            matrix=Markov().expand(matrix,m)
            matrix=Markov().inflate(matrix,r)
            #convergence condition
            if np.array_equal(matrix,prev):
                print("converged at Iternation-->",i)
                break
        clusters=Markov().get_clusters(matrix)
        print("Clusters for file-->",file)
        print(clusters)
        print len(clusters)
if __name__ == "__main__": main()