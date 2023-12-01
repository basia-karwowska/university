import numpy as np
from copy import deepcopy
import random
import Sudoku

class Sudoku2():
    def __init__(self, arg, r=None):
        if isinstance(arg, int):
            if np.sqrt(arg)-int(np.sqrt(arg))!=0: 
                raise Exception(f"Input must be a perfect square integer or a Sudoku object!")
            self.arg=arg
            self.n=arg #self.n to make it easier and not change the entire code
            #while in the arguments we give arg as it may have also Sudoku type already
            self.sn=int(np.sqrt(arg)) 
            self.table=np.zeros((arg, arg), dtype=int) 
            self.init_config()
        if isinstance(arg, Sudoku):
            if r is None:
                r=np.random.random() #fraction of the entries to keep fixed
            n_arg=arg.n
            mask=np.random.choice([True, False], size=(n_arg, n_arg), p=[r, 1-r])
            #for probability we need an array of probabilities corresponding to values
            #from the array a, here [True, False]
            
            #SHUFFLE:
            for c in range(n_arg): #column the same, we are permuting columns
                for shuffle in range(100):
                    i1=random.randint(n_arg)
                    i2=random.randint(n_arg)
                    if mask[i1][c]==False and mask[i2][c]==False:
                        arg.table[i1][c], arg.table[i2][c]=arg.table[i2][c], arg.table[i1][c]
                        
    def __repr__(self):
        return str(self.table)
    def init_config(self):
        arg=self.arg
        if isinstance(arg, int):
            n=self.n
            column=np.arange(n) 
            column=column.reshape((n, 1)) 
            self.table[:]=column 
        elif isinstance(arg, Sudoku):
            
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
            column_i=table[:, i]
            cost+=(single_cost(row_i, n)+single_cost(column_i, n))
        for si in range(sn):
            for sj in range(sn):
                subsquare=table[si*sn:(si+1)*sn, sj*sn:(sj+1)*sn] 
                cost+=single_cost(subsquare, n)
        return cost
        
    
    def propose_move(self):
        n=self.n
        table=self.table
        c=np.random.randint(n) 
        while True:
            i=np.random.randint(n_arg)
            j=np.random.randint(n)
            if i!=j and mask[i][c]==False and mask[j][c]==False:
                break
        return (c, i, j)
    
    def propose_move(self):
        if isinstance(arg, int):
            n=self.n
            table=self.table
            c=np.random.randint(n) 
            while True:
                i=np.random.randint(n)
                j=np.random.randint(n)
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
        
        si1=i//sn
        sj=c//sn 
        si2=j//sn
        
        subsquare1=table[si1*sn:(si1+1)*sn, sj*sn:(sj+1)*sn]
        subsquare2=table[si2*sn:(si2+1)*sn, sj*sn:(sj+1)*sn]
        
        old_row1=table[i][:]
        old_row2=table[j][:]
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
        
            index1=i%sn 
            index2=j%sn
            index_c=c%sn
            new_subsquare1[index1][index_c], new_subsquare2[index2][index_c]=new_subsquare2[index2][index_c], new_subsquare1[index1][index_c]
            new_cost+=(single_cost(new_subsquare1, n)+single_cost(new_subsquare2, n))
        
        return new_cost-old_cost
    
            
def greedy5(problem, n_iter=10000):
    cost=problem.cost()
    for i in range(n_iter):
        move=problem.propose_move()
        delta_cost=problem.compute_delta_cost(move)
        if delta_cost<=0: 
            problem.accept_move(move)
            cost+=delta_cost
        if cost==0:
            break
    return problem, cost

 
        
def single_cost(array, n):
    return n-np.size(np.unique(array))
