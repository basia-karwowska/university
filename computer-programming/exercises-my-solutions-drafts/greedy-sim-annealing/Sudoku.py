import numpy as np
from copy import deepcopy
import random

class Sudoku():
    def __init__(self, n):
        if np.sqrt(n)-int(np.sqrt(n))!=0: #check that a number squared gives an integer
            raise Exception(f"Input must be a perfect square integer!")
        self.n=n
        self.sn=int(np.sqrt(n)) #it must be int!!
        self.table=np.zeros((n, n), dtype=int) 
        self.init_config() #should I call it in the constructor?
    def __repr__(self):
        return str(self.table)
    def init_config(self):
        n=self.n
        column=np.arange(n) 
        column=column.reshape((n, 1)) 
        self.table[:]=column 
    def display(self):
        pass
    def copy(self):
        return deepcopy(self)
    def cost(self):
        cost=0
        n=self.n
        sn=self.sn
        table=self.table
        for i in range(n):
            row_i=table[i, :]
            column_i=table[:, i] #i think by construction column cost is 0
            cost+=(single_cost(row_i, n)+single_cost(column_i, n))
        for si in range(sn): #number of subsquares
            for sj in range(sn):
                subsquare=table[si*sn:(si+1)*sn, sj*sn:(sj+1)*sn] ####
                cost+=single_cost(subsquare, n)
        return cost
        
    
    def propose_move(self):
        n=self.n
        table=self.table
        c=np.random.randint(n) 
        while True:
            i=np.random.randint(n)
            j=np.random.randint(n)
            #if i>j:
                #i, j=j, i #is it necessary in this problem? i do not think so maybe in TSP the order of i and j matters
            if i!=j:
                break
        return (c, i, j)

    def accept_move(self, move):
        table=self.table
        c, i, j=move
        table[i][c], table[j][c]=table[j][c], table[i][c] 
    def compute_delta_cost(self, move):
        c, i, j=move
        table=self.table
        n=self.n
        sn=self.sn
        
        #here we are getting the subindices of a subsquare (snxsn) of square (nxn)
        #where (i, c )and (j, c) are located, we notice that such subindices
        #can be computed by integer division
        si1=i//sn
        sj=c//sn #these subsquares have the same column indices as
        #we are swapping entries in the column in this greedy approach
        si2=j//sn
        #we consider two slices of table, the same indices for column slices
        #but maybe different for row slices (but maybe i and j are in the same
        #subsquare, possible but we do not know so we still need to compute
        #the cost difference for the subsquares, although this may or may not change
        #the same goes for rows anyways)
        
        #we extract subsquares of the table, where (i, c) and (j, c) are located
        subsquare1=table[si1*sn:(si1+1)*sn, sj*sn:(sj+1)*sn]
        subsquare2=table[si2*sn:(si2+1)*sn, sj*sn:(sj+1)*sn]
        #we extract rows where (i, c) and (j, c) are located
        old_row1=table[i][:]
        old_row2=table[j][:]
        #we compute sum of costs of both rows and both subsquares where (i, c) 
        #and (j, c) are located; even if they are located in the same subsquare
        #we can add the cost of the same subsquare twice as then in the new_cost
        #we will also add it twice and it will simplify
        #however, we may as well add a condition that if the slices are the same
        #we add only once or even do not add at all (because swapping in such a situation
        #does not change the cost of the subsquare as it does not change the numbers present in the subsquare)
        old_cost=(single_cost(old_row1, n)+single_cost(old_row2, n))
        if si1!=si2:
            old_cost+=(single_cost(subsquare1, n)+single_cost(subsquare2, n))
      
        new_row1=old_row1.copy()
        new_row2=old_row2.copy()
        new_row1[c], new_row2[c]=new_row2[c], new_row1[c]
        new_cost=(single_cost(new_row1, n)+single_cost(new_row2, n))
        
        if si1!=si2:
            new_subsquare1=subsquare1.copy()
            new_subsquare2=subsquare2.copy()
            #indices of entries we want to swap among two subsquares from a perspective of a subquare:
            index1=i%sn 
            index2=j%sn
            index_c=c%sn
            new_subsquare1[index1][index_c], new_subsquare2[index2][index_c]=new_subsquare2[index2][index_c], new_subsquare1[index1][index_c]
            #adding new subsquare costs after modifications to the total new cost
            new_cost+=(single_cost(new_subsquare1, n)+single_cost(new_subsquare2, n))
        
        return new_cost-old_cost

#Modifying LatinSquare() to Sudoku problem involves modifications in the cost
#function as the cost function drives the algorithm and conditions the decisions
#about the acceptance of moves.       
            
def greedy4(problem, n_iter=10000):
    cost=problem.cost()
    for i in range(n_iter):
        move=problem.propose_move()
        delta_cost=problem.compute_delta_cost(move)
        if delta_cost<=0: 
            problem.accept_move(move)
            cost+=delta_cost
        if cost==0:
            break
    print(f"Final cost is: {cost}.")
    return problem

 
        
def single_cost(array, n):
    return n-np.size(np.unique(array))

