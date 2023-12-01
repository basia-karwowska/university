import numpy as np
from copy import deepcopy
import Greedy


class MaxCut:
    def __init__(self, n, init=None, seed=None):
        if not isinstance(n, int) or n<=0:
            raise Exception("Number of vertices must be a positive integer!")
        if init is None:
            init=np.zeros((n, n), dtype=float)
            for i in range(n):
                for j in range(i+1, n):
                    entry=np.random.random()
                    init[i, j]=entry
                    init[j, i]=entry
        elif not isinstance(init, np.ndarray):
            raise Exception("The argument must be a matrix!")
        if init.shape!=(n, n):
            raise Exception("The input matrix and the input number of vertices do not correspond!")
        if np.any(init!=init.T):
            raise Exception("The input matrix must be symmetric!")
        self.n=n
        self.init=init
        self.set1=np.full(n, -1)
        self.set2=np.full(n, -1)
        self.cut=np.zeros((n, n), dtype=bool) #set bool so that then you can do inverse ~
        self.init_config()

        
    def init_config(self):
        n=self.n
        init=self.init
        permutation=np.random.permutation(n)
        for el in permutation[:n//2]:
            self.set1[el]=el
        for el2 in permutation[n//2:]:
            self.set2[el2]=el2
        set1, set2=self.set1, self.set2
        for v1 in set1:
            for v2 in set2:
                if v1!=-1 and v2!=-1 and init[v1, v2]!=0: #edge exists if it's cost is greater than 0
                    self.cut[v1, v2], self.cut[v2, v1]=1, 1 #using symmetricity
                
            
        
    def __repr__(self):
        return f"Initial graph: {self.init}, Set1: {self.set1}, Set2: {self.set2}, Cut: {self.cut}"


    def cost(self):
        set1=self.set1
        set2=self.set2
        init=self.init
        c=0
        for v1 in set1:
            for v2 in set2:
                if v1!=-1 and v2!=-1:
                    c+=init[v1][v2]
        return -c
        

    def propose_move(self):
        n=self.n
        move=np.random.randint(n)
        return move


    def compute_delta_cost(self, move):
        set1=self.set1
        set2=self.set2
        init=self.init
        old=0
        new=0
        if set1[move]==move:
            for el2 in set2:
                if el2!=-1: #matrix has zero entries and symmetric so does not matter if we retrieve the entry for (move, move)
                    old+=init[move][el2]
            for el1 in set1:
                if el1!=-1:
                    new+=init[move][el1]
        elif set2[move]==move:
            for el1 in set1:
                if el1!=-1: #matrix has zero entries and symmetric so does not matter if we retrieve the entry for (move, move)
                    old+=init[move][el1]
            for el2 in set2:
                if el2!=-1:
                    new+=init[move][el2]
        delta_c=new-old
        return -delta_c

    def accept_move(self, move):
        set1=self.set1
        set2=self.set2
        init=self.init
        n=self.n
        
        if set1[move]==move:
            set1[move]=-1
            set2[move]=move
        elif set2[move]==move:
            set2[move]=-1
            set1[move]=move
        
        current_cut=self.cut[move, :]
        self.cut[move, :]=~current_cut
        self.cut[:, move]=~current_cut
        #we inverted but we want some 0's to stay uninverted, the zeros which referred
        #to the absence of link between two vertices in the original graph
        #to fix this we are running the following loop: (probably there is more efficient way)
        #we have 2 types of 0: 0's which mean that the numbers are in the same set
        #so they are not part of the cut and 0's which mean absence of the link 
        #whatsoever, so these edges are neither on the graph nor in the cut
        #we want to distinguish these cases becau
        for i in range(n):
            if init[i][move]==0:
                self.cut[i, move], self.cut[move, i]=0, 0
            

    def copy(self):
        return deepcopy(self)
    def display(self):
        pass

a=MaxCut(5)
Greedy.greedy(a)