import numpy as np

test_g1 = [
np.array([
[ 6.0, 8.0, 13.0],
]),
np.array([
[ 9.0, 15.0, np.inf],
[ 8.0, 10.0, 12.0],
[np.inf, 8.0, 7.0]
]),
np.array([
[ 15.0, np.inf],
[ 20.0, 8.0],
[np.inf, 7.0],
]),
np.array([
[ 3.0],
[ 4.0]
])
]
test_g0 = [np.array([[3.3]])]

def check_graph(g):
    
    if not isinstance(g, list):
        raise Exception("Input should be a list!")
    n=len(g)
    if n==0:
        raise Exception("The graph should not be empty!")
    if not(all(g[i].ndim==2 for i in range(n))):
        raise Exception("The subarrays of the input array must be 2-dimensional!")
    for i in range(n-1):
        if g[i].shape[1]!=g[i+1].shape[0]:
            raise Exception("The number of columns of previous subarray must correspond to the number of rows of the next subarray!")
    if not (g[0].shape[0]==1 and g[-1].shape[1]==1):
        raise Exception("The input and output layers have one node each!")
    return "All tests passed!"

def n_nodes(g):
    return sum([x.shape[0] for x in g])+1 #the last node
        
#!!!
#def label_conversion(g):
    #edge cases
    
def label_conversion_1(g, index):
    if index<0 or index>n_nodes(g):
        raise Exception("Input out of bounds, a node with such index does not exist!")
    ind=index
    layer=0
    inter_layer=0
    i=0
    while ind>0:
        ind-=g[i].shape[0]
        
        if ind<0:
            inter_layer=g[i].shape[0]+ind #abs(ind-1)
            break
        
        layer+=1
        i+=1
        #inter_layer=abs(ind) if ind=0, then by default inter-layer will be 0
        
    return (layer, inter_layer)

def label_conversion_2(g, indices):
    if indices[0]<0 or indices[0]>len(g): #the greatest layer index is equal to len(g) 
        raise Exception("Layer index out of bounds!")
    if indices[1]<0 or indices[1]>g[indices[1]].shape[0]-1: #number of rows-1 gives the maximum allowed inter-layer index
        raise Exception("Inter-layer index out of range for the corresponding layer!")
    layer, inter_layer=indices
    index=sum(g[i].shape[0] for i in range(layer))+inter_layer
    return index
        
def label_conversion_1_test():
    assert label_conversion_1(test_g1, 0)==(0, 0)
    assert label_conversion_1(test_g1, 1)==(1, 0)
    assert label_conversion_1(test_g1, 2)==(1, 1)
    assert label_conversion_1(test_g1, 3)==(1, 2)
    assert label_conversion_1(test_g1, 4)==(2, 0)
    assert label_conversion_1(test_g1, 5)==(2, 1)
    assert label_conversion_1(test_g1, 6)==(2, 2)
    assert label_conversion_1(test_g1, 7)==(3, 0)
    assert label_conversion_1(test_g1, 8)==(3, 1)
    assert label_conversion_1(test_g1, 9)==(4, 0)
    print("All assertions passed!")
    
label_conversion_1_test()


def label_conversion_2_test():
    assert label_conversion_2(test_g1, (0, 0))==0
    assert label_conversion_2(test_g1, (1, 0))==1
    assert label_conversion_2(test_g1, (1, 1))==2
    assert label_conversion_2(test_g1, (1, 2))==3
    assert label_conversion_2(test_g1, (2, 0))==4
    assert label_conversion_2(test_g1, (2, 1))==5
    assert label_conversion_2(test_g1, (2, 2))==6
    assert label_conversion_2(test_g1, (3, 0))==7
    assert label_conversion_2(test_g1, (3, 1))==8
    assert label_conversion_2(test_g1, (4, 0))==9
    print("All tests passed again!")
label_conversion_2_test()


def check_inversion():
    n=n_nodes(test_g1)
    for i in range(n):
        assert label_conversion_2(test_g1, label_conversion_1(test_g1, i))==i
    print("Function is invertible indeed!")

check_inversion()


def function(g):
    n=n_nodes(g)
    c=np.full(n, np.inf)
    n_layers=len(g) #number of layers is len(g)+1!!! but we will account for the
    #last layer with just 1 node in the additional step because we would get 
    #index out of range while calling g[i] for g[len(g)]
    c[0]=0 #0th layer is filled
    #first for loop: to consider each layer, we go forwards and build the subsequent
    #solutions on the previous, so in first iteration, we consider the layer 1
    #and in the nested for-loop we consider all the elements in the current layer
    #and in the nested for loop, we consider all possible predecessors of a given
    #node in the current layer (set of its predecessors) so nodes from the previous layer
    #and we choose the shortest distance to get from 0 through the previous layer
    #to the given node in the current layer (for any given node in the current layer, we do this process)
    #we kind of accumulate costs, for subsequent layers, we build on the solution
    #to the previous layer, while for the previous, we built on the solution
    #to the previous to that
    whence=np.full(n, -1)
    for i in range(1, n_layers): #we go over all layers subsequent to 0 and compute
    #the shortest path from the starting node to all nodes of this layer
    #we consider the previously computed shortest paths between the starting node
    #and all the nodes of the previous layer as well as the cost associated with
    #the edge connecting particular nodes of the previous layer with particular
    #nodes of the current layer; we store these costs in c
        n_layer_elements=g[i].shape[0] #we want to iterate over all elements of 
        #a particular layer which we are currently considering in the iteration of the outer loop
        n_sources=g[i-1].shape[0] #we will consider all possible connections
        #between the nodes in the current layer and the previous layer
        #and minimize over possible costs associated with pair configurations
        for j in range(n_layer_elements):
            best_k_to_j=np.inf #for each node in the current layer, we initialize
            #best cost to np.inf; for each node in the current layer, we will
            #compute costs over all possible sources (by considering the sum of
            #the minimum cost to get to a particular node in the previous layer plus
            #the cost of an edge connecting this node in the previous layer with
            #the node which we are currently considering in the current layer) 
            #we will update best_k_to_j if the cost to get to current node is better
            for k in range(n_sources):
                converted_index_source=label_conversion_2(g, (i-1, k))
                curr_k_to_j=g[i-1][k, j]+c[converted_index_source] 
                #object c is of length corresponding to the number of nodes
                #so it has usual indexing, hence we need to use index conversion
                #to retrieve the cost of the kth node in the previous (i-1)th layer
                #we also add the cost of an edge connecting kth node (row index) in the
                #previous (i-1)th layer to the jth node (column index) in the next layer
                if curr_k_to_j<best_k_to_j:
                    converted_index_dest=label_conversion_2(g, (i, j))
                    best_k_to_j=curr_k_to_j
                    whence[converted_index_dest]=converted_index_source
            #having gone through all possible sources for the current node and computed
            #the minimum cost to do so, we add the computed cost to c structure
            #which gathers minimum costs to get to any node from the zero node
            c[label_conversion_2(g, (i, j))]=best_k_to_j
       
    n_sec_to_last=g[-1].shape[0]
    best_last=np.inf
    best_ind=-1
    for l in range(n_sec_to_last):
        ind_=label_conversion_2(g, (n_layers-1, l))
        last_=c[ind_]++g[-1][l, 0] #only 1 "column", 0th, i.e. all arrays g[-1][l] have one element for all l
        if last_<best_last:
            best_last=last_
            best_ind=ind_
    whence[-1]=best_ind
    c[-1]=best_last
        
    '''
    n_sec_to_last=g[-1].shape[0]
    last_edges=np.array([x[0] for x in g[-1]]) #array with costs of edges
    #we create it that way because g is 3-dim array so g[-1] would be 2-dim:
    #[[4], [3]] but we want 1-dim, just a list [4, 3] as then we can add
    #it to another list and perform the minimization
    last_vertices_cumulative=c[-n_sec_to_last-1:-1]
    costs_to_final_node=last_edges+last_vertices_cumulative #costs to consider 
    #are costs to get to all nodes in the previous layer from the starting point pkus
    #the cost associated with the edge from the previous layer to the current
    #layer from particular previous node
    c[-1]=min(costs_to_final_node) #minimize over possible lengths
    pred_of_last=np.where(costs_to_final_node==c[-1])[0] #retrieving the inter-layer
    #index (argmin), so the predecessor of the last node in the optimal path
    whence[-1]=label_conversion_2(g, (n_layers-1, int(pred_of_last)))
    '''
    
    
    #Reconstructing the path:
    
    path=np.zeros(n_layers+1)
    path[-1]=n-1 #n was number of nodes
    path[0]=0
    for i in range(n_layers-1, 0, -1):
        path[i]=whence[int(path[i+1])] ##int and float issues with indexing so we convert
    
    return c[-1], path, whence
            #min(g[i-1][:, j]+c[label_conversion_2((i-1, ))])
        
    
'''
if ind==0:
layer+=1
inter_layer=0
if ind<0:
layer+=1
inter_layer=abs(ind)
'''
        
        
        
#auxiliary test function
    




'''
Creating an ndarray from ragged nested sequences (which is a list-or-tuple of lists-or-tuples-or ndarrays with different lengths or shapes) is deprecated. If you meant to do this, you must specify 'dtype=object' when creating the ndarray
*** ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
'''






def function2(g):
    n=n_nodes(g)
    n_layers=len(g) #n_layers is in fact len(g)+1
    whence=np.full(n, -1, dtype=int) #fix data type at the beginning to avoid the issues later
    prev=g[0]
    shape=prev.shape[1]
    whence_index=1
    for i in range(n_layers-1): #from 0 to n_layers-1 cause we consider i+1 so
    #we want to start from g[1] (as we initialized g[0], so we move on) and 
    #we want to finish on g[n_layers-1] but since it is i+1, i+1=n_layers-1
    #so we want to finish with i=n_layers-2
        nxt=np.min(prev, axis=0).reshape(shape, 1)+g[i+1]
        argmins=np.argmin(prev, axis=0)
        whence_index_end=whence_index+argmins.size
        whence[whence_index:whence_index_end]=np.array([label_conversion_2(g, (i, j)) for j in argmins])
        whence_index=whence_index_end
        prev=nxt
        shape=prev.shape[1]
    minimum=min(prev)[0]
    whence[-1]=label_conversion_2(g, (n_layers-1, np.argmin(prev))) #n_layers-1 but n_layers is the number of n_layers-1 by construction
    #n_layers is index of last layer while n_layers-1 is index of second to last
    path=np.zeros(n_layers+1)
    path[-1]=n-1 
    path[0]=0
    for i in range(n_layers-1, 0, -1):
        path[i]=whence[int(path[i+1])]
        
    return minimum, path
        
        
'''  
        n_layer_elements=g[i].shape[0] 
        n_sources=g[i-1].shape[0] 
        for j in range(n_layer_elements):
            best_k_to_j=np.inf 
            for k in range(n_sources):
                converted_index_source=label_conversion_2(g, (i-1, k))
                curr_k_to_j=g[i-1][k, j]+c[converted_index_source] 
                if curr_k_to_j<best_k_to_j:
                    converted_index_dest=label_conversion_2(g, (i, j))
                    best_k_to_j=curr_k_to_j
                    whence[converted_index_dest]=converted_index_source
            c[label_conversion_2(g, (i, j))]=best_k_to_j
       
    n_sec_to_last=g[-1].shape[0]
    best_last=np.inf
    best_ind=-1
    for l in range(n_sec_to_last):
        ind_=label_conversion_2(g, (n_layers-1, l))
        last_=c[ind_]++g[-1][l, 0] 
        if last_<best_last:
            best_last=last_
            best_ind=ind_
    whence[-1]=best_ind
    c[-1]=best_last

    
    path=np.zeros(n_layers+1)
    path[-1]=n-1 
    path[0]=0
    for i in range(n_layers-1, 0, -1):
        path[i]=whence[int(path[i+1])]
    
    return c[-1], path
'''


def filled(n, x, typ=float):
    a = np.zeros(n, dtype=typ)
    a.fill(x)
    return a

def gen_graph_like(g, x0 = 0.0, x = np.inf, typ=float):
    return [filled(1, x0, typ)] + [filled(gl.shape[1], x, typ) for gl in g]


#cost structure mimicking the graph

def function3(g):
    c=gen_graph_like(g)
    whence=gen_graph_like(g, x0=0, x=-1, typ=int) #we will keep track from which index we moved
    n=len(c) #len of graph+1
    for i in range(1, n):
        c0=c[i-1]
        c1=c[i]
        for j in range(len(c1)):
            for k in range(len(c0)):
                min_=c0[k]+g[i-1][k, j]
                if min_<c1[j]:
                    c[i][j]=min_
                    whence[i][j]=k
    path=[]
    indd=0
    for ind in range(n-1, 0, -1): #index of whence; excluding 0 because from 1 we get info about 0
        path.append(label_conversion_2(g, (ind, whence[ind][indd])))
        indd=whence[ind][indd]
    
    return c[-1], path
        #c[i][:]=np.min(c[i-1]+g[i-1], axis=1)