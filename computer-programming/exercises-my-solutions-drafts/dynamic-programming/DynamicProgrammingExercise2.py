import numpy as np
a=np.zeros(5)
def minimum_dynamic(arr):
    n=len(arr)
    if n==1:
        return arr[0]
    #best=np.inf
    if arr[0]<minimum_dynamic(arr[1:]):
        return arr[0]
    else:
        return minimum_dynamic(arr[1:])
    

def minimum_rec1(arr):
    n=len(arr)
    if n==0:
        return np.inf
    else:
        return min(arr[0], minimum_dynamic(arr[1:]))
    
def minimum_rec2(arr):
    n=len(arr)
    if n==0:
        return np.inf
    else:
        return min(arr[n-1], minimum_rec2(arr[:n-1]))

def minimum_dp1(arr):
    n=len(arr)
    min_=np.inf
    for i in range(n):
        if arr[i]<min_:
            min_=arr[i]
    return min_

def minimum_dp2(arr):
    n=len(arr)
    min_=np.inf
    min_pos=-1
    for i in range(n):
        if arr[i]<min_:
            min_=arr[i]
            min_pos=i
            #decisions[i]=1
    return min_, min_pos #, decisions

def get_minimum_index_dp2(decisions):
    n=len(decisions)
    for i in range(n-1, -1, -1): #iterate backwards
        if decisions[i]==1:
            return i
    return -1

#recursive method, with indices returned
def minimum_rec3_2(arr):
    n=len(arr)
    if n==0:
        return (np.inf, -1)
    min_subarr, min_index=minimum_rec3_2(arr[:n-1])
    if arr[n-1]<min_subarr: #in the backward pass
        return (arr[n-1], n-1)
    else:
        return min_subarr, min_index
    
       # return min(arr[n-1], minimum_rec2(arr[:n-1]))
   

#you could introduce offset instead of doing global variables
i=0
l=-1
def minimum_rec3_1(arr):
    n=len(arr)
    global l
    l+=1
    #length of the original array
    if n==0:
        return np.inf, -1
    min_subarr, min_index=minimum_rec3_1(arr[1:])
    if arr[0]<min_subarr:
        global i
        i+=1
        return arr[n-i], l-i
    else:
        return min_subarr, min_index
        
 

def test():
    random_array=np.random.random(10)
    assert min(random_array)==minimum_dp1(random_array)
    
test()