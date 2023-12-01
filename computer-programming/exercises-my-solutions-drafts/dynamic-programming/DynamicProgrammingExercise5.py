import numpy as np

test_w1=np.array([[1.0, 1.0, 1.0, 1.0], [2.0, 1.0, 2.0, 3.0], [0.0, 1.0, 2.0, 0.0], [0.0, 0.0, 0.5, 3.0], [2.0, 1.0, 1.0, 0.0]])
test_w2=np.array([[1.0, 3.0, 0.0], [2.0, 1.0, 7.0], [4.0, 1.0, 3.0], [1.0, 4.0, 2.0]])

def optimal_pass(w):
    if w.size==0:
        raise Exception("The matrix cannot be empty!")
    if (w>=0).sum()!=w.size:
        raise Exception("The matrix cannot have negative entries.")
    n, m=w.shape
    c=np.zeros((n, m))
    whence=np.zeros((n, m)) #top left corner sentinel value of 0
    whence[1:, 0]=1
    whence[0, 1:]=-1
    
    #numpy broadcasting instead of for loop
    c[:, 0]=w[:, 0].cumsum()
    '''
    for i in range(n):
        c[i, 0]=w[:i+1, 0].sum()
    '''
    c[0, :]=w[0, :].cumsum()
    '''
    for j in range(m):
        c[0, j]=w[0, :j+1].sum()
    '''
    #we keep filling the matrix c for small submatrices and we are using
    #the information for submatrices for the bigger matrix
    for i in range(1, n):
        for j in range(1, m): #probably my code favours move down over move to the left
        #in the case of equal costs becase the first argument of min is from up
            c[i, j]=w[i, j]+min(c[i-1][j], c[i][j-1]) #we have already computed
    #optimal path to get to c[i-1][j] and c[i][j-1] so we now just need to
    #decide whether to go to c[i, j] through the optimal path to c[i-1][j]
    #or through the optimal path corresponding to c[i][j-1] and we ofc
    #add the cost of the current entry w[i, j]
            whence[i, j]=(-1)**(np.argmin([c[i-1][j], c[i][j-1]]))
    #Reconstructing the path:
    path=[]
    direct=whence[n-1, m-1]
    row_ind=n-1
    col_ind=m-1
    while direct!=0: #or while row_ind!=0 or col_ind!=0; sentinel value of 0 is in whence[0, 0]
        path.append(direct)
        if direct==-1:
            col_ind-=1
        elif direct==1:
            row_ind-=1
        direct=whence[row_ind, col_ind]
    path.reverse()
    path=np.array(path)
    
    assert len(path)==n+m-2
    assert path.sum()==(n-1)-(m-1)
    
    cum_sum=w[0, 0]
    row_ind=0
    col_ind=0
    for direction in path:
        if direction==1:
            row_ind+=1
        elif direction==-1:
            col_ind+=1
        cum_sum+=w[row_ind, col_ind]
    assert cum_sum==c[-1, -1]
    
    return c[-1, -1], path
#c collects cumulative costs

'''
def opt_pass_debug(path):
    optimal_pass
'''
        

