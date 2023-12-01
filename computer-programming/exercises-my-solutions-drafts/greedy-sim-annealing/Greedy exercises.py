import numpy as np
import matplotlib.pyplot as plt

#%% EXERCISE 1 RECREATING TSP
#The input is cities, each separated by some distance and the output is the route, 
#we want to create the class for an input, manipulate it to obtain the desired optimal output.

#Generate random configuration of n cities (we choose only the number of cities
#and the class will create a map of cities, assigning to each of the cities 
#x- and y-coordinate, we may want to input these distances manually so there
#are optional arguments x, which is a list of x-coordinates of cities with corresponding
#indices and y, which is a list of y-coordinates).
#Writing "class Cities(n, x=None, y=None)" is VERY WRONG, WE NEED TO WRITE ARGUMENTS
#IN INIT, CITIES HAS NO ARGUMENTS unless it's inheriting or sth

class Cities():
    def __init__(self, n, x=None, y=None, seed=None):
        if ((not isinstance(n, int)) and (n>4)): #INCLUDE THIS PART!!! YOU SKIPPED IT!!!
            raise Exception("n needs to be an int > 4!")
        if seed is not None: rnd.seed(seed) #INITIALIZE RANDOM NUMBER GENERATOR TO A GIVEN STATE, PAST CONFIGURATION CORRESPONDING TO SEED
        self.n=n
        self.config=np.array([i for i in range(n)])
        self.init_config()
        if x is None: #if the first default argument is not changed, then the second neither
            self.x=np.random.random(n)
            self.y=np.random.random(n)
        elif y is None: #we can have situation of x being not None and y being None 
        #if we input only argument for x; we do either elif y is None or if y is None and x is not None
            self.y=np.random.random(n)
        else:
            self.x=x
            self.y=y
    
    #def init_config(self): #THIS CAN BE 
        #n=self.n
        #self.config[:]=np.random.permutation(n)
    def __repr__(self):
        return f"Cities configuration is {self.config}"

def display(cities):
    plt.clf()
    x=cities.x
    y=cities.y
    config=cities.config
    x_ordered=x[config] #indexing using another array
    y_ordered=y[config]
    plt.plot(x, y, "o", color="red") #plotting single points
    plt.plot(x_ordered, y_ordered, color="red") 
    plt.plot([x_ordered[0], x_ordered[-1]], [y_ordered[0], y_ordered[-1]], color="red")
    plt.pause(0.01)
    
    
    
def propose_move(cities):
    n=cities.n
    e1=np.random.randint(n)
    e2=np.random.randint(n)
    while True:
        if e1>e2:
            e1, e2=e2, e1
        if e2!=e1+1 and e2%(n-1)!=e1: #we do not want to swap neighbouring edges nor the same edge with itself
        #since the configuration is a cycle, 0 and last are neighbours
        #e2%(n-1)!=e1 avoids swapping the same node and first with last
        #e2!=e1+1 avoids swapping neighbouring nodes
            break
    return (e1, e2)
     
def accept_move(cities, move):
    e1, e2=move
    cities.config[e1+1:e2+1]=cities.config[e2:e1:-1] #not that efficient, reversing order of a subarray
#swapping means connecting the first node of e1 to the first node of e2 and the second node of e1 to the second node of e2

def distance(cities, node1, node2):
    return np.sqrt((cities.x[node1]-cities.x[node2])**2+(cities.y[node1]-cities.y[node2])**2)

'''
    #coordinates of node1
    x1=cities.x[node1]
    y2=cities.y[node1]
    x2=cities.x[node2]
    y2=cities.y[node2]
'''
    
    
#We can just deal with the function cost_difference, but we may want to know
#the total cost and then upon accepting move updating it by the cost difference.
    
def cost_difference(cities, move): #length of e1+length of e2 vs length of 2 new edges
    e1, e2=move
    n=cities.n
    config=cities.config
    v1e1=config[e1] #vertex 1 of edge e1
    v2e1=config[e1+1] #vertex 2 of edge e1
    v1e2=config[e2] #vertex 1 of edge e2
    v2e2=config[(e2+1)%(n-1)] #vertex 2 of edge e2
    cost_old_edges=distance(cities, v1e1, v2e1)+distance(cities, v1e2, v2e2)
    cost_new_edges=distance(cities, v1e1, v1e2)+distance(cities, v2e1, v2e2)
    return cost_new_edges-cost_old_edges

def total_cost(cities):
    n=cities.n
    config=cities.config
    cost=0
    for city_id in range(n):
        cost+=distance(cities, city_id, (city_id+1)%(n-1))
    return cost
               

#we have as input a particular initial configuration of cities
#and the idea of this algorithm is to search for two nodes (propose the move)
#and accept the move if it improves the situation, i.e. if it reduces cost
#pick start

def greedy(cities, n_iter=10): 
    display(cities)
    cost=total_cost(cities)
    print(f"Initial cost is {cost}.")
    print(f"Initial configuration is {cities.config}.")
    for i in range(n_iter):
        move=propose_move(cities) 
        delta_cost=cost_difference(cities, move)
        if delta_cost<=0:
            accept_move(cities, move)
            cost+=delta_cost
            print(f"Current cost is {cost}")
            print(f"Current configuration is {cities.config}.")
    display(cities)
    print(f"Final cost is {cost}.")
    print(f"Final configuration is {cities.config}.")
    return cities, total_cost(cities)
    


