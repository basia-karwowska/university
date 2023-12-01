import numpy as np
from copy import deepcopy
import random

class LatinSquare2():
    def __init__(self, n):
        self.n=n
        self.table=np.zeros((n, n), dtype=int) 
        self.init_config()
    def __repr__(self):
        return str(self.table)
    def init_config(self):
        n=self.n
        column=np.arange(n) 
        column=column.reshape((n, 1)) #reshape returns an array, not modifies in place
        self.table[:]=column #using broadcasting, columns with numbers from 0 to 4
    def display(self):
        pass
    def copy(self):
        return deepcopy(self)
    def cost(self):
        cost=0
        n=self.n
        table=self.table
        for i in range(n):
            row_i=table[i, :]
            column_i=table[:, i]
            cost+=(single_cost(row_i, n)+single_cost(column_i, n))
        return cost
    def propose_move(self):
        n=self.n
        table=self.table
        c=np.random.randint(n) #column to permute, extract a random column
        #extract two different random rows
        while True:
            i=np.random.randint(n)
            j=np.random.randint(n)
            if i>j:
                i, j=j, i
            if i!=j:
                break
        return (c, i, j)
        '''
        while True:
            v=np.random.randint(n)
            if v!=table[x][y]:
                break
        numbers_1=np.array([i for i in range(value)])
        numbers_2=np.array([i for i in range(value+1, n)])
        numbers=np.hstack((numbers_1, numbers_2))
        v=np.random.choice(numbers)
        return (x, y, v)
        '''
    def accept_move(self, move):
        table=self.table
        c, i, j=move
        table[i][c], table[j][c]=table[j][c], table[i][c] #modifying the view modifies the original array viewed
        #swapping of two numbers
    def compute_delta_cost(self, move):
        c, i, j=move
        table=self.table
        n=self.n
        
        old_row1=table[i][:]
        old_row2=table[j][:]
        old_cost=single_cost(old_row1, n)+single_cost(old_row2, n)
        
        #deep copy, modify the deep copies of rows and columns
        new_row1=old_row1.copy()
        new_row2=old_row2.copy()
        new_row1[c], new_row2[c]=new_row2[c], new_row1[c]
        new_cost=single_cost(new_row1, n)+single_cost(new_row2, n)
        return new_cost-old_cost
        
        
            
def greedy2(problem, n_iter=10000):
    cost=problem.cost()
    for i in range(n_iter):
        move=problem.propose_move()
        delta_cost=problem.compute_delta_cost(move)
        if delta_cost<=0: #we also allow for equality
            problem.accept_move(move)
            cost+=delta_cost
        if cost==0:
            break
    return problem, cost



        
        
        
    
        
        
def single_cost(array, n):
    return np.size(np.unique(array))!=n #Returns True (1), which we want to add to cost
#if not all elements are unique