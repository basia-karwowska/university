import numpy as np
test_a=np.array([-2, 1, -3, 4, -1, 2, 1, -5, 4])

def max_subarray_extensive(a):
    n=len(a)
    #edge cases
    if n==0:
        return 0.0, (-1, -1)
    greater_than_zero=(a>0)
    if greater_than_zero.sum()==n:
        return a.sum(), (0, n-1)
    if greater_than_zero.sum()==0:
        return 0.0, (-1, -1)
    max_s=-np.inf
    ind=(-1, -1) #sentinel values
    '''
    for i in range(n):
        for j in range(i+1, n):
            s_i_j=a[i:j+1].sum()
            if s_i_j>max_s:
                max_s=s_i_j
                ind=(i, j)
    '''
    #use cumulative sum to obtain all the sums of the subarrays that start from i
    for i in range(n):
        cum_sums_i=np.cumsum(a[i:])
        max_=max(cum_sums_i)
        ind_=list(max_).index() #this outputs the index of subarray
        indices=(i, i+ind_)
        if max_>max_s:
            max_s=max_
            ind=indices
    '''
    for i in range(n):
        cumul_from_i=np.cumsum(a[i:])
        best_j=np.argmax(cumul_from_i)
        best_s=cumul_from_i[best_j]
        if best_s>max_s:
            max_s=best_s
            ind=(i, i+best_j)
    '''
            
    
            
   #computational complexity is still of order n: 1 loop and cumulative sum of order n
        
    return max_s, ind


#3 cases: maximum is in the left subarray, right or crosses
#call the same function on the array on the left
#on the right
#recursion, divide and conquer
#base case length 1


#IN DIVIDE AND CONQUER SUBPROBLEMS ARE NOT SHARED SO WE DO NOT MEMOIZE


#here subproblems are not repeated so we do not need memoization and can apply
#divide and conquer strategy
def max_subarray_DnC(a):
    #base case of length 1
    n=len(a)
    
    if n==1:
        if a[0]>0:
            return a[0], a
        else:
            return 0.0, np.array([])
    #a) call the function on the left half
    #b) call the function on the right half
    mid=n//2
    max_left, sa_left=max_subarray_DnC(a)
    max_right, sa_right=max_subarray_DnC(a)
    
    ##c) compute the best crossing sub-array #moving from mid to the left and
    #to the right with arrows in opposite direction, the one to the left subarray
    #and the other in the direction of the right subarray to compute the
    #best crossing subarrays
    cumul_right=np.cumsum(a[mid:])
    best_j_r=np.argmax(cumul_right)
    best_s_r=cumul_right[best_j_r]
    cumul_left=np.cumsum(a[mid-1::-1]) #we are going backwards, cumulative sums
    best_j_l=np.argmax(cumul_left)
    best_s_l=cumul_left(best_j_l)
    max_cross=best_s_l+best_s_r
    sa_cross=a[mid-1-best_j_l:mid+best_j_r+1] #these are the indices of the actual array
    M=max(max_left, max_right, max_cross)
    if M==max_left:
        return M, sa_left
    elif M==max_right:
        return M, sa_right
    else:
        return M, sa_cross
    #from mid-1
    #we know the sums of the best half on the right and on the left
    #but again we need to shift the indices as they do not correspond to actual
    #indices of  the array
    '''
    for i in range(n):
        max_crossing, sa_crossing=max_subarray_DnC(a[:i])[0]+max_subarray_DnC(a[i:])[0], 
        if max_>max_s:
            max_s=max_
            ind=indices
    '''
            
            
        
        
    
    #return best between a, b, c