import numpy as np
from copy import deepcopy
import random

class LatinSquare():
    def __init__(self, n):
        self.n=n
        self.table=np.zeros((n, n), dtype=int) 
        #creating a container for configuration, important to specify data type as default is float64
        self.init_config()
    def __repr__(self):
        return str(self.table)
    def init_config(self):
        n=self.n
        self.table[:]=np.array([[np.random.randint(n) for i in range(n)] for j in range(n)])
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
        x=np.random.randint(n)
        y=np.random.randint(n)
        value=table[x][y]
        '''
        while True:
            v=np.random.randint(n)
            if v!=table[x][y]:
                break
        '''
        #is it the right method statistically - verify
        numbers_1=np.array([i for i in range(value)])
        numbers_2=np.array([i for i in range(value+1, n)])
        numbers=np.hstack((numbers_1, numbers_2))
        v=np.random.choice(numbers)
        return (x, y, v)
    def accept_move(self, move):
        table=self.table
        x, y, v=move
        self.table[x][y]=v #in accept move function we do not set conditions for acceptance but we just accept
        #in greedy we will set conditions for acceptance
        #if v not in table[:, y] and v not in table[x, :]: #and or or?
            #self.table[x][y]=v
    def compute_delta_cost(self, move):
        x, y, v=move
        table=self.table
        n=self.n
        
        old_column=table[:][y]
        old_row=table[x][:]
        old_cost=single_cost(old_column, n)+single_cost(old_row, n)
        
        #deep copy, modify the deep copies of rows and columns
        new_column=old_column.copy()
        new_row=old_row.copy()
        new_column[x]=v
        new_row[y]=v
        new_cost=single_cost(new_column, n)+single_cost(new_row, n)
        return new_cost-old_cost
        
        
            
def greedy(problem, n_iter=10000):
    cost=problem.cost()
    for i in range(n_iter):
        move=problem.propose_move()
        delta_cost=problem.compute_delta_cost(move)
        if delta_cost<=0: #we also allow for equality to be able to explore more and do not get stuck?
            problem.accept_move(move)
            cost+=delta_cost
        if cost==0:
            break
    return problem, cost



        
        
        
    
        
        
def single_cost(array, n):
    return np.size(np.unique(array))!=n #Returns True (1), which we want to add to cost
#if not all elements are unique