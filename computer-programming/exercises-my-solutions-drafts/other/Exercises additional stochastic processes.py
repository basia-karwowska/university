import numpy as np

def simple_process(n_repet=10000):
    C=np.array([[0, 0.5, 0], [1, 0, 1], [0, 0.5, 0]]) #proposal matrix
    A=np.array([[0, 1, 0], [0.25, 0, 0.5], [0, 1, 0]]) #acceptance matrix
    values=np.arange(3)
    frequencies=np.zeros(3)
    curr=np.random.randint(0, 3)
    frequencies[curr]+=1
    for i in range(n_repet):
        new_curr=np.random.choice(values, p=C[:, curr]) #column of source gives probabilities of destinations
        if np.random.random()<A[new_curr, curr]:
            curr=new_curr
        frequencies[curr]+=1
    estimated_probability=frequencies/n_repet
    return estimated_probability
        
        
def drunk_guys_33(n_iters=10000, n_guys=100):
    C=np.array([[0, 1/2, 0, 1/2, 0, 0, 0, 0, 0], [1/3, 0, 1/3, 0, 1/3, 0, 0, 0, 0],
               [0, 1/2, 0, 0, 0, 1/2, 0, 0, 0], [1/3, 0, 0, 0, 1/3, 0, 1/3, 0, 0],
               [0, 1/4, 0, 1/4, 0, 1/4, 0, 1/4, 0], [0, 0, 1/3, 0, 1/3, 0, 0, 0, 1/3],
               [0, 0, 0, 1/2, 0, 0, 0, 1/2, 0], [0, 0, 0, 0, 1/3, 0, 1/3, 0, 1/3], 
               [0, 0, 0, 0, 0, 1/2, 0, 1/2, 0]]) 
    C=C.T #I messed up
    A=np.array([[0, 0.66666667, 0, 0.66666667, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0.75, 0, 0, 0, 0],
       [0, 0.66666667, 0, 0, 0, 0.66666667, 0, 0, 0], [1, 0, 0, 0, 0.75, 0, 1, 0, 0], 
       [0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 1, 0, 0.75, 0, 0, 0, 1], [0, 0, 0, 0.66666667, 0, 0, 0, 0.66666667, 0],
       [0, 0, 0, 0, 0.75, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0.66666667, 0, 0.66666667, 0]])
    A=A.T
    positions=np.random.randint(0, 9, n_guys)
    frequencies=np.unique(positions, return_counts=True)
    
    #defining freq and freq_single_guys
    freq=np.zeros(9)
    freq_single_guys=np.zeros((n_guys, 9))
    for i in range(len(frequencies[0])):
        freq[frequencies[0][i]]=frequencies[1][i]
        #you should not do this: freq[frequencies[0, i]]=frequencies[1, i]
        #because it is not indexing row and column of the same array but indexing
        #an array from a tuple of array and then indexing element of this array
    for guy in range(n_guys):
        freq_single_guys[guy, positions[guy]]+=1
        
    for attempt in range(n_iters):
        for guy in range(n_guys):
            curr=positions[guy]
            new_curr=np.random.choice(9, p=C[:, curr])
            if np.random.random()<A[new_curr, curr]:
                curr=new_curr
            freq_single_guys[guy, curr]+=1
            freq[curr]+=1
    estimate_total=freq/(n_guys*n_iters)
    estimate_individual=freq_single_guys/n_iters
    print(f"Overall probability distribution estimate is: {estimate_total}.")
    print(f"Single guy probability distributions estimates are: {estimate_individual}.")
    return estimate_total, estimate_individual
    
        