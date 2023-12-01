import numpy as np
from copy import deepcopy
import SimAnn

def cost_row_col(arr, s):
    return abs(arr.sum()-s)

def diag_cost(matrix, s):
    return abs(matrix.trace()-s)
    
def right_diag_cost(matrix, s):
    rev_cols=matrix[:, ::-1]
    return abs(rev_cols.trace()-s)
    

class MagicSquare:
    def __init__(self, n, s, square=None, seed=None):
        if seed is None: seed=np.random.seed()
        self.n=n
        self.s=s
        '''
        if square is None:
        '''
        self.square=np.zeros((n, n), dtype=int)
        self.init_config()
        '''
        we want to replace repeated elements
        elif square.size!=(np.unique(square)).size():
            c=np.unique(square, return_counts=True)
            unique_elements=c[0][c[1]==1]
            repeated_elements=c[0][c[1]!=1]
            repeated_elements_indices
        '''
            
            
        #square=self.square
        #self.col_diff=square.sum(0)-s
        #self.row_diff=square.sum(1)-s
        #self.diag_diff=np.array([np.trace(square)-s, np.trace(square[::-1])-s])
        #self.temporary_diff=np.zeros(3, dtype=int)
        
        
    def init_config(self):
        s, n=self.s, self.n
        a=np.zeros((n, n))
        fill_values=np.arange(-n**2+s//n, n**2+s//n, step=2)
        #in the initial configuration we want the average of numbers to be s//n
        #so that it is possible to get n*(n//n)=s on diagonals, rows and columns
        #we want to fill the entries with n^2 distinct numbers so to simplify
        #the situation, our initial configuration will be numbers from 
        #-n**2+s//n, n**2+s//n
        for i in range(n):
            a[i, :]=fill_values[i*n:(i+1)*n]
            #a[i, :]=np.linspace((-2*s)//n, (2*s)//n, )
            #a[i, :]=np.arange(i*(s-n), (i+1)*(s+n), step=2)
            #a[i, :]=np.arange(i*(s-n), (i+1)*(s+n), step=2)
            #to have numbers closer already, 2n numbers between s+n and s-n
            #so we do step2
            #a[i, :]=np.arange(i*n, (i+1)*n)
        np.random.shuffle(a.ravel())
        self.square[:]=a 
        #we do not have constraints but we want initial configuration that is close to the true one
        #also without repeated entries so we use this method
        
    def cost(self):
        square, n, s=self.square, self.n, self.s
        if np.size(np.unique(square))!=n*n:
            return np.inf
        cost_col_row=(abs(s-square.sum(0))+abs(s-square.sum(1))).sum()
        cost_diag=diag_cost(square, s)+right_diag_cost(square, s)
        '''
        sum_diag1=0
        sum_diag2=0
        for i in range(n):
            sum_diag1+=square[i, i]
            sum_diag2+=square[i, n-i]
        cost_diag=(abs(s-sum_diag1)+abs(s-sum_diag2))
        '''
        total_cost=cost_col_row+cost_diag
        return total_cost
   
            
        '''
        total_cost=(abs(square.sum(0)-s)).sum()+(abs(square.sum(1)-s)).sum()
        #adding diagonal elements (right diagonal obtained by reading rows from bottom
        #to top, flipping the array top-bottom, while columns are not switched, only
        #the order of entries in columns is)
        total_cost+=(abs(np.trace(square)-s))+(abs(np.trace(square[::-1])-s))
        '''
        '''
        total_cost=abs(col_diff).sum()+abs(row_diff).sum()+abs(diag_diff).sum()
        return total_cost
        '''
    def propose_move(self):
        n, s=self.n, self.s
        i=np.random.randint(n)
        j=np.random.randint(n)
        nr=np.random.randint(-3*s//n, 5*s//n, dtype=np.int64) #easier when we restrict the range, but not too tightly
        return (i, j, nr)
    def compute_delta_cost(self, move):
        i, j, nr=move
        square, s, n=self.square, self.s, self.n
        
        if nr in square: #we do not allow for repetitions
            return np.inf
        #we compute portion of old_cost relevant to this change to compute delta
        old_cost=cost_row_col(square[i, :], s)+cost_row_col(square[:, j], s)
        if i==j:
            old_cost+=diag_cost(square, s)
        if i==n-1-j: #not elif because for one entry (in the middle of the matrix)
        #it is both part of one as well as another diagonal so has twofold impact
        #on the total cost (in fact fourfold because of row, column and both diagonal)
            old_cost+=right_diag_cost(square, s)
            
        #temporary change square[i, j] to nr, store old_nr to return to it
        #as only in move acceptance we mutate
        old_nr=square[i, j] #this is not a view so it is safe to store it and then
        #we will be able to return, extracting one entry and assigning is not a view
        #that is why we can manipulate as follows without a need for deepcopy
        square[i, j]=nr
        new_cost=cost_row_col(square[i, :], s)+cost_row_col(square[:, j], s)
        if i==j:
            new_cost+=diag_cost(square, s)
        if i==n-1-j:
            new_cost+=right_diag_cost(square, s)
        square[i, j]=old_nr
        
        return new_cost-old_cost
            
        
        
        
        
        '''
        
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
        '''
    
    
    def accept_move(self, move):
        i, j, nr=move
        self.square[i, j]=nr
        '''
        temp=self.temporary_diff
        self.col_diff+=temp[1]
        self.row_diff+=temp[0]
        self.diag_diff+=temp[2]
        '''
        
    def display(self):
        pass
    
    def copy(self):
        return deepcopy(self)
    
    
msq = MagicSquare(6, 150, seed=789)

best = SimAnn.simann(msq, mcmc_steps=5*10**4, seed=266,
                     beta0=1.0, beta1=2.0, anneal_steps=30)

np.set_printoptions(threshold=np.inf) # force numpy to print the whole table
print(f"final best configuration:\n{best}\ncost={best.cost()}")

if best.cost() == 0:
    print("FOUND A VALID ASSIGNMENT")
else:
    print("NOT SOLVED")