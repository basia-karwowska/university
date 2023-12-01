import numpy as np


test_0_v=np.array([3, 7, 2, 10])
test_0_s=5



#minimum, that is why we initialize to sentinel value n+1
def subset_sum_improved(v, s):
    n=len(v)
    w=np.full(s+1, n+1) 
    w[0]=0 #we initialize it to 0
    #w will give us the maximum index (excluding the element corresponding to it)
    #of the slice which contains elements summing to a desired sum so if
    #w[sum_]=j, then the subarray of minimum length starting from v[0]
    #that contains elements summing to sum_ is v[:j] (v[j] element excluded)
    
    for sum_ in range(1, s+1):
        for ind_ in range(1, n+1):
            rest=sum_-v[ind_-1] #we consider whether to include v[ind_-1] or not
            print(f"Rest is {rest}, difference is {sum_-v[ind_-1]}, v[ind_-1] is {v[ind_-1]}")
            #if the subarray of subarray v[:ind_-1] sums to rest, i.e. if there
            #is a minimum index for this array to sum to rest (if it is not a
            #sentinel value n+1, and rest+v[ind_-1]=sum_, then we can compute
            #the minimum index of the subarray of v that sums to a given sum_
            #by taking the maximum over 1) the minimum possible index of the last
            #element of a subarray that sums to rest (computed in one of the 
            #previous steps and encoded in w, i.e. we can access it by w[rest]);
            #2) index of a currently considered element (it may be already included
            #in the subarray that has elements summing to rest since it is not sorted
            #but not necessarily, that is why we take max of those indices
            #and that gives the minimum index of the last element of a subarray
            #that sums to a given sum_)
            
            if rest>=0 and w[rest]!=n+1: #if it is not sentinel value
            #first we check if rest>=0 before we proceed to any indexing
            #also since entries in v are positive, rest<sum, so we have a 
            #guarantee that rest is a valid index if it is greater than 0
            #as it cannot exceed sum_
                print(f"Condition satisfied: now ind_ is {ind_} and w[rest] is {w[rest]}")
                w[sum_]=max(ind_, w[rest]) #if the minimum index of a subarray 
                print(f"We selected {w[sum_]}")
                print(f"Now w is {w}")
                break #we want to break since now we already found the minimum ind_
                #such that a subarray v[:ind_] sums to a given sum_
                
                #to sum to the remainder is greater than the index, we take w[rest]
                #as we also want all elements from subarray that sums to rest
                #to be included as well as an elemenet v[ind_-1]
                #note that even if rest==0, then w[rest]=0, initialized to sentinel
                #value and then max(ind_, 0)=ind_, we want to initialize w[0]
                #not as n-1 as 0 is allowed, we do not want to disregard it
    if w[s]==n+1: #it did not get updated which implies there is no subset
        #where we can find elements that sum up to s
        return None
    #BACKTRACKING TO GET INDICES GIVEN WHENCE STRUCTURE:
    inds=[]
    ss=s
    while ss!=0: #or w[ss] != 0
        j=w[ss]-1
        inds.append(j)
        ss-=v[j]
    inds.reverse()
    return inds #pay attention to indentation, you need to return after executing the external loop
                
        

def subset_sum(v, s):
    #rows of m give the possible sums up until s and columns of m give the sizes
    #of subsets
    if not isinstance(v, np.ndarray) and not isinstance(v, list): #pay attention to "or" and "and"
        raise Exception("Input must be a vector!")
    if isinstance(v, list):
        v=np.array(v)
    if v.ndim!=1:
        raise Exception("Input array must be 1-dimensional!")
    if (v>0).sum()!=v.size:
        raise Exception("All elements of an input vector must be strictly positive!")
    if v.dtype!=int:
        raise Exception("All elements of the input vector must be integers!")
    '''
    for el in v:
        if el<=0 and not isinstance(el, int):
            raise Exception("All elements of an input vector must be strictly positive integers!")
    '''
    if s<0 or not isinstance(s, int):
        raise Exception("Subset sum must be a positive integer!")
        
    n=v.size   
    m=np.zeros((s+1, n+1), dtype=bool)
    m[0, :]=True
    for row in range(1, s+1): #rows are particular sums #columns are #row 0 is preallocated
        for col in range(1, n+1): #cols gives the sizes of subsets
            rest=row-v[col-1] #we keep track of indices, they are translated by 1
            if rest>=0 and m[rest, col-1]==True: #if we have subset of size col summing to particular value,
            #we have subset of size col-1 summing to the rest (this value ss-element for which the subset
            #sums to the desired value for the first time), then we set all values to the right equal to True
            #in fact the process of going forward guarantees accuracy here
            #we subtract
                m[row, col:]=True #ofc the first column except for the first entry 
#remains False as preallocated, as we cannot find a subset of 0 elements summing up to value greater than 0
    if m[-1, -1]==False: #or in general if there are no Truths in the last row (corresponding to ss=s)
        return None
#!!! My approach:
    #the idea is that: index of the first True in the last row (corresponding to s)
    #allows to find the entry which is part of the subset_sum equal to s 
    #and the subsequent entries of this sum can be found by looking for the index of the first True
    #in the row equal to s-v[index of the previous True-1]=s-rest
    #we continue this procedure until all the terms we have found sum up to s
    sum_=s
    indices_=[]
    while sum_>0: #we do not do sum!=0 because we can get to negative values
        index=(n+1-np.sum(m[sum_, :])-1) #n+1 #since truths appear from some index on to the right
        #we get get the number of truths by summing the entries in the respective row
        #(with index sum_) and then to get the column index of the first Truth in
        #the row, we subtract this sum from the index of the last column (n, as there are n+1 cols) and then
        #to get the index of the corresponding element in the vector, we subtract 1
        #so basically we have n-np.sum(m[sum_, :])
        #THE FIRST appearance of truth in the row corresponds to the index of interest
        #because adding this element to the sum results in obtaining the specified s
        #ofc all elements to the right (sets including these subsets) also have
        #elements summing to s but to get info which element needed to be added
        #we look at the first appearance of Truth in a particular row
        indices_.append(index)
        sum_-=v[index] #now we will look for the first Truth in the row given 
        #by the updated sum, after subtracting an element included in the sum_
    indices_.reverse()
    indices_=np.array(indices_)
    
    whence=np.full((s+1, n+1), -1)
    #whence[m]=n-np.sum(m, axis=1)
    
    for ss in range(1, s+1):
        if m[ss, :].sum()!=0:
            whence_ind=n-m[ss, :].sum()+1
            whence_val=whence_ind-1
            whence[ss, whence_ind:]=whence_val
    
    #Backtracking whence:
    
    sum_2=s
    ind=whence[-1, -1]
    indices2_=[]
    while ind!=-1: #or sum_2!=0
        indices2_.append(ind)
        sum_2-=v[ind]
        ind=whence[sum_2, ind]
    indices2_=np.array(indices2_)
    
    assert (indices_<=n-1).sum()==indices_.size and (indices_>=0).sum()==indices_.size and v[indices_].sum()==s
    return m, indices_, indices2_
            
    #guarantee is that we fill all to the right!