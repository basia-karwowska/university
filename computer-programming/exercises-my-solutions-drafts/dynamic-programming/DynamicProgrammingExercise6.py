import numpy as np
test_w_1 = [14, 3, 27, 4, 5, 15, 11]
test_w_2 = [14, 3, 27, 4, 5, 15, 1]

def max_skipped_subset(arr):
    n=len(arr)
    if n==0:
        return 0, []
    if n==1:
        return arr[0], 0
    v=np.zeros(n)
    whence=np.zeros(n) #instead of n-2 in order to not have negative dimensions in case of corner cases
    v[0]=arr[0]
    v[1]=max(arr[0], arr[1])
    whence[0]=1
    whence[1]=np.argmax([arr[0], arr[1]]) #1 if we accepted arr[1] and 0 if we skipped
    #inside argmax we give a list
    for i in range(2, n): #note that indices of whence are translated relative to indices of v
    #whence contains less elements by 2
        if v[i-1]>=v[i-2]+arr[i]:
            whence[i]=0
            v[i]=v[i-1]
        elif v[i-1]<v[i-2]+arr[i]:
            whence[i]=1
            v[i]=v[i-2]+arr[i]
            
    #backtracking
    subset=[]
    inds=[]
    index=n-1
    while index>=0:
        if whence[index]==1: #this means that we accepted the corresponding element
            subset.append(arr[index])
            inds.append(index)
            index-=2
        elif whence[index]==0: #that means we skipped the corresponding element of a set, instead considering previous
            subset.append(arr[index-1])
            inds.append(index)
            index-=3
    #subset.reverse()
    subset.sort()
    inds.reverse()
    subset=np.array(subset, dtype=float)
    print(f"Subset is: {subset}")
    print(f"v is {v}")
    return v[-1], subset, inds


w1=test_w_1
s1=max_skipped_subset(test_w_1)[0]
inds=max_skipped_subset(test_w_1)[2]
def checksolution(w, s, inds):
    assert float(w[inds].sum())==float(s) #indexing with a list
    #equal with floating point precision
    assert inds
    np.diff
    
        
