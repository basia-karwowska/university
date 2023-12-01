import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from copy import deepcopy, copy
import SimAnn
import Greedy


class MaxCut:
    def __init__(self, g, seed=None):
        if not (isinstance(g, np.ndarray) and (g==np.transpose(g)).all()):
            #but this assumes that g and transpose have the same dimensions but
            #in fact we should make an additional check for a square matrix
            #e.g. g.ndim==2 and g.shape[0]==g.shape[1]
            #we cannot write just "g==np.transpose(g))" because this will return
            #a matrix of boolean values, entry-wise comparison; this however
            #will verify if all are True, thus if for entries of g equal all entries
            #of g trapose (way to check that a matrix is symmetric!): (g==np.transpose(g)).all()
            raise Exception("g needs to be a numpy array and a symmetric matrix!")
        if seed is not None: rnd.seed(seed)
        self.g=-1*g #matrix representing the graph, costs of edges, we want to
        #multiply the costs by -1 as our greedy algorithm and simulating annealing
        #which we would like to be able to apply to MaxCut, determines the minimum
        #but in maxcut problem we are searching for maximum, so minimum of negative
        #total cost of the cut will correspond to the maximum of the cost of the cut
        self.n=g.shape[0] #number of vertices
        #atribute g of object of class MaxCut is just negative of the matrix representing the input graph
        #initial configuration:
        n=self.n
        ## creating containers for vertices, we want to put vertices from the
        #first set in s1 at index corresponding to the label of the vertex
        #and vertices from the second set in s2 at index corresponding to value
        #that way it will be easy to add and delete
        #we create container of "-1" as it is number which does not correspond
        #to any index and it is negative number so it is easy to see that the
        #smallest potential sum of entries of s1 and s2 is -n, but we do not allow
        #this case as then it means we do not have cut at all, two sets must be
        #non-empty; -1 at some position in a set (np.array but u know what i mean)
        #will mean that a particular element with label corresponding to that 
        #position does not belong to this set
        #WRONG IF sum.s1==-n or sum.s2=-n
        self.s1=np.full(n, -1)
        self.s2=np.full(n, -1)
        self.init_config()
        self.mask=(self.s1>=0) #we read the mask from the initial configuration
    
        
    def init_config(self): #do not call this method outside, only once it should
    #be called in the constructor, it is constructor specific, otherwise our properties
    #will not be satisfied
        n=self.n
        while True: #we want to make sure that both sets are non-empty, so that
        #there is at least 1 True in the mask and at least 1 True in ~mask
        #so s1 can have at least 1 vertex and complementary set s2 should also have at least 1 vertex
            r=np.random.random()
            if 0<int(r*n)<n:
                break
        vertices=np.arange(n)
        #generate a random mask for the first set
        mask=np.zeros(n, dtype=bool)
        mask[:int(n*r)]=True
        np.random.shuffle(mask)
        self.s1[mask]=vertices[mask] #we assign vertices to s1 at the corresponding positions 
        self.s2[~mask]=vertices[~mask] #we assign the remaining vertices to s2 also at the corresponding positions


    def display(self):
        pass

    def propose_move(self): #move proposal will simply consist in generating
    #a random vertex to move from 1 set to another bearing in mind the constraints
    #we cannot propose an invalid move which could make one of the sets empty
    #i.e. if move is in s1 (which we can easily check by reading s1[move] because
    #by construction we made s1[move]=move if the entry is in s1 and s1[move]=-1 
    #if the entry is in s2); we want neither of sets to be empty as a result of
    #potential acceptance of the proposed move, which in other words means that
    #we do not want to choose move (which we define as a vertex to move from one set to another in
    #the case of this problem), such that this vertex is not the only vertex in the
    #set; by construction we know that move is the only vertex if the set s1
    #if s1[move]=move and all other entries are "-1", i.e. if the sum of entries
    #of s1 is move+(n-1)*(-1)=move+1-n or if np.unique(a) is [-1, move] or [move, -1]
        n=self.n
        s1=self.s1
        s2=self.s2
        while True:
            move=np.random.randint(n)
            if (s1[move]==move and s1.sum()!=1-n+move) or (s2[move]==move and s2.sum()!=1-n+move):
                break
        return move      

    def accept_move(self, move):
        #move is either in s1 or s2
        s1=self.s1
        s2=self.s2
        if s1[move]==move:
            s1[move], s2[move]=-1, move
            self.mask[move]=False #we need to change mask as well!!!
        else:
            s1[move], s2[move]=move, -1
            self.mask[move]=True
        

    def cost(self):
        g=self.g
        s1=self.s1
        s2=self.s2
        mask=self.mask
        c=0.0
        #we only want to iterate through entries present in each array
        for v1 in s1[mask]:
            for v2 in s2[~mask]:
                c+=g[v1, v2]
        return c

    def copy(self):
        return deepcopy(self)
    #symmetric matrix - does not matter whether we compute m_{ij} or m_{ji}
    #but sometimes we need to be consistent and not double-count
    def compute_delta_cost(self, move):
        delta_c=0.0
        mask=self.mask
        g=self.g
        s1=self.s1
        s2=self.s2
        if s1[move]==move:
            #we do not care about subtracting/adding g[move, move] as all diagonal
            #elements of the symmetric matrix representing a graph are 0 because
            #edges do not connect vertex to itself
            for v2 in s2[~mask]:
                delta_c-=g[move, v2] #now "move" will be in s2 so we discard all
                #the edges connecting "move" and all elements of s2 because these
                #edges will no longer be in the cut
            for v1 in s1[mask]: #now "move" will be in s2 so we have to compute
            #the added cost of new edges, cost of edges connecting "move" and all vertices in s1
                delta_c+=g[move, v1]
        else:
            for v1 in s1[mask]:
                delta_c-=g[move, v1]
            for v2 in s2[~mask]:
                delta_c+=g[move, v2]
        return delta_c
            

def rnd_symmetric(n):
    m=np.full((n, n), -1.0, dtype=float) #FIX DTYPE!! OF THE CONTAINER, IT IS 
    #CRITICAL, BECAUSE OTHERWISE, PYTHON WILL ROUND RANDOMLY GENERATED NUMBERS TO 0
    for i in range(n-1):
        m[i][i]=0
        for j in range(i+1, n):
            r=np.random.random()
            m[i, j], m[j, i]=r, r
    m[n-1, n-1]=0 #fixing last entry 
    return m
 
        
graph=rnd_symmetric(12)
mxc=MaxCut(graph)
'''
best = SimAnn.simann(mxc, mcmc_steps=10**4, seed=58473625,
                     beta0=0.1, beta1=10.0, anneal_steps=20)
print(best)
best_greedy=Greedy.greedy(mxc)
print(best_greedy, 50, 50)
'''