import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import time

#with class TSP we can move everything to methods because it is self-sufficient class now
#in showing the Hamiltonian paths; class Cities contained only information about
#the number of cities and their coordinates, while TSP says more as it also contains configuration attribute!


class TSP5(): #has more attributes than Cities(); it has number of cities, 
#cities coordinated (relative positions) as well as configuration
    def __init__(self, n, x=None, y=None, seed=None):
        if ((not isinstance(n, int)) and (n>4)): 
            raise Exception("n needs to be an int > 4!")
        if seed is not None: np.random.seed(seed)
        self.n=n
        #self.config=np.array([i for i in range(n)]) #it cannot be passed as an argument as this is what
        #we want to find and do not know so it does not make sense to put it in the arguments
        self.config=np.zeros(n, dtype=int)
        self.init_config()
        if x is None: 
            self.x=np.random.random(n)
            self.y=np.random.random(n)
        elif y is None: 
            self.y=np.random.random(n)
        else:
            self.x=x
            self.y=y
    def init_config(self):
        n=self.n
        self.config[:]=np.random.permutation(n)
    def display(self):
        x, y, config=self.x, self.y, self.config
        plt.clf()
        plt.plot(x, y, "o", color="red") #plotting single points
        plt.plot(x[config], y[config], color="red") #plotting links between
        #points by indexing arrays of points by array containing the permutation
        #giving the desired order of links
        #we connect points (defined by their coordinates) in the order given by
        #the current configuration of TSP
        comeback=[config[-1], config[0]] # or config[n-1] instead of config[-1]
        plt.plot(x[comeback], y[comeback], color="red")
        plt.pause(0.001)
    def propose_move(self):
        n=self.n
        while True:
            e1=np.random.randint(n)
            e2=np.random.randint(n)
            if e1>e2:
                e1, e2=e2, e1
            if e2!=e1+1 and e2%(n-1)!=e1:
                break
        return (e1, e2)
    def accept_move(self, move):
        e1, e2=move
        self.config[e1+1:e2+1]=self.config[e2:e1:-1]
#!!! we could also do config=self.config, and then config[e1+1:e2+1] = config[e2:e1:-1] as modifying view changes array
    def distance(self, city1, city2):
        x=self.x
        y=self.y
        return np.sqrt((x[city1]-x[city2])**2+(y[city1]-y[city2])**2)
    
    def cost_difference(self, move):
        e1, e2=move
        n=self.n
        v1e1=self.config[e1] #vertex 1 of edge e1
        v2e1=self.config[(e1+1)%n] #%n not necessary #vertex 2 of edge e1; why do we have to write %n although
        #we have a guarantee that e1 is edge previous to e2 so it shouldn't go out of bounds
        v1e2=self.config[e2] #vertex 1 of edge e2
        v2e2=self.config[(e2+1)%n] #vertex 2 of edge e2
        cost_old_edges=self.distance(v1e1, v2e1)+self.distance(v1e2, v2e2)
        cost_new_edges=self.distance(v1e1, v1e2)+self.distance(v2e1, v2e2)
        return cost_new_edges-cost_old_edges
    
    '''
    def cost_difference(self, move):
        c_old = self.total_cost()
        new_probl = self.copy()
        new_probl.accept_move(move)
        c_new = new_probl.total_cost()
        return c_new - c_old
    '''
    
    def total_cost(self):
        n=self.n
        config=self.config
        cost=0.0
        for i in range(n):
            cost+=self.distance(config[i], config[(i+1)%n]) 
        return cost
    def copy(self): 
        return deepcopy(self)  
    
    '''
    ALTERNATIVELY WITH DEEP COPY DELTA_COST
    
    def copy(self):
        return deepcopy(self)


    def delta_cost(self, move):
        c_old = self.cost()
        new_probl = self.copy()
        new_probl.accept_move(move) # accept the move leads to modifying the configuration
        c_new = new_probl.cost()
        return c_new - c_old

    '''
       

def greedy5(problem, n_iter=10, n_restarts=10, seed=None): 
    if seed is None:
        np.random.seed(seed)
        
    best_route_global=None
    best_cost_global=np.inf

    for j in range(n_restarts):
        problem.init_config() #tsp also has initial configuration while initialized
        #but we need to change initial configuration upon each restart as we want to start from different points
        #that's the idea of runs of the algorithm, different initialization,
        #while iterations allow to explore more and more moves starting within one run of the algo
        #display(cities, route)
        print(1, problem.config)
        cost=problem.total_cost()
        for i in range(n_iter):
            move=problem.propose_move() 
            delta_cost=problem.cost_difference(move)
            if delta_cost<=0:
                problem.accept_move(move)
                print(2, problem.config)
                cost+=delta_cost
        if cost<best_cost_global: 
            best_cost_global=cost
            #best_route_global=TSP #.config #IT IS NOT SAFE
            best_route_global=problem.copy()
            print(3, problem.config, best_route_global.config)
            #print(f"Current cost is {best_cost_global}")
            #print(f"Current configuration is {best_route_global}.")
            #TSP.display()      
    problem.display()
    print(f"Final configuration: {best_route_global.config}, final cost: {best_cost_global}.")
    #print(f"Final cost is {best_cost_global}.")
    #print(f"Final configuration is {best_route_global}.")
    return best_route_global

t1=time.time()
a=TSP5(10)
b=greedy5(a)
t2=time.time()
print(f"TSP5 and greedy5 TIME = {t2-t1}") 

'''
Final configuration: [5 6 1 9 7 4 8 0 2 3], final cost: 3.42324717476915.
TSP5 and greedy5 TIME = 0.27654242515563965
'''

#SEE WHAT HAPPENS WHEN best_route_global=TSP.config
'''
when we do best_route_global=TSP:
    
a=TSP(10)
a.config
output: array([2, 7, 3, 1, 5, 8, 6, 9, 0, 4])
best=greedy3(a)
best.config
output: array([5, 8, 9, 0, 2, 4, 1, 7, 6, 3])
a.config
output: array([5, 8, 9, 0, 2, 4, 1, 7, 6, 3])
a.config[0]=0
a.config
output: array([0, 8, 9, 0, 2, 4, 1, 7, 6, 3])
best.config
output: array([0, 8, 9, 0, 2, 4, 1, 7, 6, 3])

'''


''' WITH DEEPCOPY

d=TSP(10)

d.config
Out[13]: array([2, 3, 6, 1, 9, 0, 8, 5, 4, 7])

e=greedy3(d)

d.config
Out[15]: array([6, 7, 2, 9, 5, 0, 8, 3, 4, 1])

e.config
Out[16]: array([1, 8, 6, 3, 4, 9, 5, 2, 7, 0])


'''