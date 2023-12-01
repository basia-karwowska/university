import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from copy import deepcopy 

class TSP:
    def __init__(self, n, seed=None):
        if ((not isinstance(n, int)) and (n>4)):
            raise Exception("n needs to be an int > 4!")
        if seed is not None: rnd.seed(seed)
        x = rnd.rand(n)
        y = rnd.rand(n)
        self.x, self.y = x, y
        self.n = n
        self.route = np.zeros(n, dtype=int) 
        self.init_config() 

    def dist(self, city1, city2):
        x, y = self.x, self.y
        x1, y1 = x[city1], y[city1]
        x2, y2 = x[city2], y[city2]
        return np.sqrt((x1-x2)**2 + (y1-y2)**2)

    def init_config(self):
        n = self.n
        self.route[:] = rnd.permutation(n) 
        
    def display(self): 
        x, y, n, route = self.x, self.y, self.n, self.route
        plt.clf()
        plt.plot(x, y, 'o', color="black")
        plt.plot(x[route], y[route], color='orange')
        comeback = [route[n-1], route[0]]
        plt.plot(x[comeback], y[comeback], color='orange')
        plt.pause(0.001)

    def cost(self):
        n, route = self.n, self.route
        c = 0.0
        for edge in range(n):
            city1, city2 = route[edge], route[(edge+1) % n]
            c += self.dist(city1, city2)
        return c

    def copy(self): 
        return deepcopy(self)

#INHERITANCE
#WE WANT TO CHANGE MOVES SO WE GET RID OF METHODS WHICH DEPENDED ON THE MOVE,
#I.E. DELTA_COST, PROPOSE_MOVE AND ACCEPT_MOVE


class TSP_SC(TSP): #CLASS NOT DEF!!!
    #def __init__(self, n, seed=None):
        #TSP.__init__(self, n, seed=None)
    def propose_move(self):
        n=self.n
        while True:
            i=np.random.randint(n)
            j=np.random.randint(n)
            if i>j:
                i, j=j, i
            if i!=j:
                break
        move=(i, j)
        return move
    def accept_move(self, move):
        i, j=move
        route=self.route
        route[i], route[j]=route[j], route[i]
    def delta_cost(self, move):
        new=self.copy()
        new.accept_move(move)
        old_cost=self.cost()
        new_cost=new.cost()
        return new_cost-old_cost
    def copy(self):
        return deepcopy(self)
    
    def delta_cost2(self, move):
        #i and j, prev_i, prev_j, nxt_i, nxt_j are city labels, numbers which
        #allow to locate city on the map given their coordinates, unchanged
        #while ii, ij are indices of cities on the route, reflecting relative positioning
        i, j=move
        n=self.n 
        a=np.where(self.route==i)[0] #broadcasting used to find the index of element
        b=np.where(self.route==j)[0]
        ii=a[0]
        ij=b[0]
        prev_i=self.route[ii-1] #number (label) of the city neighbouring with old i, preceding it
        nxt_j=self.route[(ij+1)%n] #here indices of cities in the route, indices of permuted cities do not correspond to city labels
        #although the set of city labels is the same as set of indices in the list of cities
        #PERMUTATION, bijection, do not confuse
        nxt_i=self.route[ii+1]
        prev_j=self.route[ij-1]
        #if j==i+1 or j==i+2 or j%(n-1)==i or j%(n-1)==i+1 or j%(n-2)==i: #for cities neighbouring or 1 apart
        if ij==ii+1 or ij==ii+2: #more compact for cases of neighbours and almost neighbours
            new_edges=self.dist(j, prev_i)+self.dist(i, nxt_j) #negative indices allowed
            old_edges=self.dist(i, prev_i)+self.dist(j, nxt_j) #(nxt_j)%n
        elif (ij==n-1 and ii==0) or (ij==n-1 and ii==1) or (ij==n-2 and ii==0): #j%(n-1)==i or (j+1)%(n-1)==i or j%(n-2)==i:
            new_edges=self.dist(j, nxt_i)+self.dist(i, prev_j) #j-1, i+1 
            old_edges=self.dist(i, nxt_i)+self.dist(j, prev_j)
        else:
            new_edges=self.dist(prev_i, j)+self.dist(nxt_i, j)+self.dist(prev_j, i)+self.dist(nxt_j, i) #here you don't have modulo!!! ((nxt_j)%n, i)
            #we are dealing with indices of cities in route but also with labels of cities, also expressed as numbers and there is no reason to change them
            #distinguish between these two!!
            old_edges=self.dist(prev_i, i)+self.dist(nxt_i, i)+self.dist(prev_j, j)+self.dist(nxt_j, j)
        return new_edges-old_edges
#if j is the last index, next index is 0 so mod, but if i is 1st index previous index is -1 and it works as we may have negative indexing
            
#we do nxt_i i+1 prev i-1 the same for j   
    
class TSP_CL(TSP):
    def propose_move(self):
        n = self.n
        while True:
            e1 = rnd.randint(n)
            e2 = rnd.randint(n)
            if e2 < e1: e1, e2 = e2, e1
            if (e2 != e1 and e2 != e1+1 and (e2+1) % n != e1): break
        move = (e1, e2) 
        return move
    def accept_move(self, move): 
        route = self.route
        e1, e2 = move 
        route[e1+1:e2+1] = route[e2:e1:-1] 
    def delta_cost(self, move):
        c_old = self.cost()
        new_probl = self.copy()
        new_probl.accept_move(move)
        c_new = new_probl.cost()
        return c_new - c_old
    
    
    
    
        






# INTERFACE
# By turning all the functions into mehtods of the problem, greedy is now generic and can be applied to any problem where we defined:
#   init_config
#   display
#   cost
#   delta_cost
#   propose_move
#   accept_move

def greedy(probl, num_iters=1, num_restarts=1, seed=None):
    if seed is not None: rnd.seed(seed)

    best_probl = None
    best_c = np.inf

    for i in range(num_restarts):
        print()
        print(f"trial {i+1}")
        probl.init_config() 
        c = probl.cost()
        print(f"intial cost = {c}")
        for t in range(num_iters):
            move = probl.propose_move() 
            delta_c = probl.delta_cost(move) 
            if delta_c <= 0:
                probl.accept_move(move)
                c += delta_c
                print(f"t={t} -> new cost = {c}")
        print(f"final cost = {c}")

        if c < best_c:
            best_c = c
            best_probl = probl.copy() 
            
    print(f"best score = {best_c}")
    best_probl.display()
    
    return best_probl




'''
a=TSP_SC(10, seed=123)

b=TSP_CL(10, seed=123)

a.route
Out[35]: array([6, 2, 5, 9, 4, 3, 1, 7, 0, 8])

b.route
Out[36]: array([6, 2, 5, 9, 4, 3, 1, 7, 0, 8])

greedy(a, 10, 10, seed=1234)

best score = 2.7871322439479775

greedy(b, 10, 10, seed=1234)

best score = 2.8429520896965057
'''
