import numpy as np
from copy import deepcopy
import SimAnn


class MagicSquare:
    def __init__(self, n, s, seed=None):
        if seed is None: seed=np.random.seed()
        self.n=n
        self.s=s
        self.square=np.zeros((n, n), dtype=int)
        self.init_config()
        square=self.square
        self.col_diff=square.sum(0)-s
        self.row_diff=square.sum(1)-s
        self.diag_diff=np.array([np.trace(square)-s, np.trace(square[::-1])-s])
        self.temporary_diff=np.zeros(3, dtype=int)
    def init_config(self):
        s, n=self.s, self.n
        self.square[:]=np.random.randint(s, size=(n, n))
        #we do not have constraints but we want initial configuration that is close to the true one
    def cost(self):
        square, n, s=self.square, self.n, self.s
        if np.size(np.unique(square))!=n*n:
            return np.inf
        col_diff=self.col_diff
        row_diff=self.row_diff
        diag_diff=self.diag_diff
        '''
        total_cost=(abs(square.sum(0)-s)).sum()+(abs(square.sum(1)-s)).sum()
        #adding diagonal elements (right diagonal obtained by reading rows from bottom
        #to top, flipping the array top-bottom, while columns are not switched, only
        #the order of entries in columns is)
        total_cost+=(abs(np.trace(square)-s))+(abs(np.trace(square[::-1])-s))
        '''
        total_cost=abs(col_diff).sum()+abs(row_diff).sum()+abs(diag_diff).sum()
        return total_cost
    def propose_move(self):
        n=self.n
        i=np.random.randint(n)
        j=np.random.randint(n)
        nr=np.random.randint(-10000000, 10000000, dtype=np.int64)
        return (i, j, nr)
    def compute_delta_cost(self, move):
        i, j, nr=move
        square=self.square
        
        if nr in square:
            return np.inf
        
        n=self.n
        old_row_diff=self.row_diff[i]
        old_col_diff=self.col_diff[j]
        if i==j or i==n-1-j:
            old_diag_diff=self.diag_diff[int(i!=j)] #then index 0 when i==j and 1 if i=n-1-j   
        old_nr=square[i, j]
        
        delta_cost=0
        
        if old_row_diff*(old_nr-nr)>0: #if old difference is negative, we need a greater number to bring old difference closer to 0
            delta_cost-=abs(old_nr-nr)
            self.temporary_diff[0]=abs(old_nr-nr)
        elif old_row_diff*(old_nr-nr)<0:
            delta_cost+=abs(old_nr-nr)
            self.temporary_diff[0]=abs(old_nr-nr)
        if old_col_diff*(old_nr-nr)>0:
            delta_cost-=abs(old_nr-nr)
            self.temporary_diff[1]=abs(old_nr-nr)
        elif old_col_diff*(old_nr-nr)<0:
            delta_cost+=abs(old_nr-nr)
            self.temporary_diff[1]=abs(old_nr-nr)
        if (i==j or i==n-1-j) and old_diag_diff*(old_nr-nr)>0:
            delta_cost-=abs(old_nr-nr)
            self.temporary_diff[2]=abs(old_nr-nr)
        elif (i==j or i==n-1-j) and old_diag_diff*(old_nr-nr)<0:
            delta_cost+=abs(old_nr-nr)
            self.temporary_diff[2]=abs(old_nr-nr)  
        square[i, j]=old_nr
        return delta_cost
    
    def accept_move(self, move):
        i, j, nr=move
        self.square[i, j]=nr
        temp=self.temporary_diff
        self.col_diff+=temp[1]
        self.row_diff+=temp[0]
        self.diag_diff+=temp[2]
        
    def display(self):
        pass
    
    def copy(self):
        return deepcopy(self)
        
                
        
        
        
        
        
'''       
        
msq = MagicSquare(6, 150, seed=789)

best = SimAnn.simann(msq, mcmc_steps=5*10**4, seed=266,
                     beta0=1.0, beta1=2.0, anneal_steps=30)

np.set_printoptions(threshold=np.inf) # force numpy to print the whole table
print(f"final best configuration:\n{best}\ncost={best.cost()}")

if best.cost() == 0:
    print("FOUND A VALID ASSIGNMENT")
else:
    print("NOT SOLVED")
'''