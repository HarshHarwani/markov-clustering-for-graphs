__author__ = 'hharwani'
import sys
import numpy as np
import os

# Markov Class
class Markov:

    def normalize(self,adjacencyMatrix):
        adjacencyMatrix = adjacencyMatrix/np.sum(adjacencyMatrix,axis = 0)
        return adjacencyMatrix

    # method for expanding the matrix
    def expand(self,A, M):
        return np.linalg.matrix_power(A,M)

    # method for inflating the matrix
    def inflate(self,A, R):
        return self.normalize(np.power(A,R))

    # method for getting the clusters
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


# Utility class
class Util:
    def createAdjMatrix(Self,initalMatrix,firstColumn,secondColumn):
        for i in range(firstColumn.size):
            x=firstColumn[i]
            y=secondColumn[i]
            # connecting edges, as it is undirected graph edge is set both ways.
            initalMatrix[x][y]=1.0
            initalMatrix[y][x]=1.0
            # Adding self loops
            initalMatrix[x][x]=1.0
            initalMatrix[y][y]=1.0
        # removing the extra row and column
        initalMatrix=np.delete(initalMatrix, 0, 0)
        initalMatrix=np.delete(initalMatrix, 0, 1)
        return initalMatrix

    def buildCluMap(self,clusters):
        custMap={}
        for key in clusters:
            listele=clusters.get(key)
            for ele in listele:
                custMap[ele]=key
        return custMap


    def calculateModularity(self,clusters,adjacencyMatrix):
        intraSum=0
        interSum=0

        for key in clusters:
            list=clusters.get(key)
            intraSum+=self.calculateIntraClusterDist(list,adjacencyMatrix)

        for i in range(len(clusters)):
            list=clusters.get(i)
            interSum+=self.calculateInterClusterDist(i,list,adjacencyMatrix,clusters)

        return intraSum-interSum

    def calculateIntraClusterDist(self,list,adjacencyMatrix):
        sum=0
        for i in range(len(list)):
            ele=list[i]
            for j in range(i+1,len(list)):
                if adjacencyMatrix[i][j]==1:
                    sum+=1
        return sum

    def calculateInterClusterDist(self,i,list,adjacencyMatrix,clusters):
        sum=0
        for j in range(i+1,len(clusters)):
            listinner=clusters.get(j)
            for ele in list:
                for ele1 in listinner:
                    if adjacencyMatrix[ele][ele1]==1:
                        sum+=1
        return sum

    def calculateIntraClusterDist(self,list,adjacencyMatrix):
        sum=0
        for i in range(len(list)):
            ele=list[i]
            for j in range(i+1,len(list)):
                if adjacencyMatrix[i][j]==1:
                    sum+=1
        return sum

    def createAndWriteCluFile(self,clusters,file,max):
        custMap=self.buildCluMap(clusters)

        # removing the file if its already exists
        if os.path.exists(file):
            os.remove(file)
         # getting the fileObject
        fileObject = open(file, 'w')
        fileObject.write("*Partition PartitionName")
        fileObject.write("\n")
        fileObject.write("*Vertices "+str(int(max)))
        fileObject.write("\n")

        # building map which stores which node is in which cluster
        for key in custMap:
            fileObject.write(str(custMap.get(key)))
            fileObject.write("\n")
def main():
    files=["new_att.txt","new_collaboration.txt","new_yeast.txt"]
    for file in files:
        basename = os.path.basename(file)
        filename = os.path.splitext(basename)
        myfile_name_without_suffix = filename[0]
        print "For file ",file
        edges = np.loadtxt(file)
        # taking the max from the array to create new matrix of required dimension
        max=np.amax(edges)

        # extracting two columns from the original two dimensional array
        firstColumn=edges[:,0]
        secondColumn=edges[:,1]

        # creating the initial empty array, creating one extra dimension to start the index from 1.
        initalMatrix=np.ndarray(shape=(max+1,max+1))
        for m in range(2,7):
            for r in np.arange(1.1,2.2,0.2):
                # creating the adjacencyMatrix
                adjacencyMatrix=Util().createAdjMatrix(initalMatrix,firstColumn,secondColumn)

                # normalizing the matrix
                matrix=Markov().normalize(adjacencyMatrix)
                #configuration paramters
                max_loop=1000
                iterations=0
                for i in range(max_loop):
                    iterations+=1
                    # maintaining a previous copy for checking convergence
                    prev = matrix.copy();
                    matrix=Markov().expand(matrix,m)
                    matrix=Markov().inflate(matrix,r)
                    # convergence condition
                    if np.array_equal(matrix,prev):
                        print("converged at Iternation-->",i)
                        break
                # getting the clusters from the matrix
                clusters=Markov().get_clusters(matrix)
                Util().createAndWriteCluFile(clusters,myfile_name_without_suffix+".clu",max)
                modularity=Util().calculateModularity(clusters,adjacencyMatrix)
                print(" M=>"+str(m)+" R=>"+str(r)+" no of clusters=> "+str(len(clusters))+" Modularity=>"+str(modularity)+" Iterations "+str(iterations))
                print("================================================================================================")

if __name__ == "__main__": main()