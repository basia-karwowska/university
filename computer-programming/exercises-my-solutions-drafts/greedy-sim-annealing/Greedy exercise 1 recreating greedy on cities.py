import numpy as np
import matplotlib.pyplot as plt

#Recreating cities, preparatory code for TSP. 

class Cities():
    def __init__(self, n, x=None, y=None, seed=None):
        #!!! CITIES ARE JUST POINTS ON THE MAP, SO WE JUST NEED THE ATTRIBUTE NUMBER OF CITIES
        #AND X- AND Y-COORDINATES OF EACH CITY (POINT)
        if ((not isinstance(n, int)) and (n>4)): #!!! INCLUDE THIS PART!!! 
            raise Exception("n needs to be an int > 4!")
        if seed is not None: np.random.seed(seed) #!!! INITIALIZE RANDOM NUMBER GENERATOR TO A GIVEN STATE, PAST CONFIGURATION CORRESPONDING TO SEED
        self.n=n
        if x is None: #if the first default argument is not changed, then the second neither
            self.x=np.random.random(n)
            self.y=np.random.random(n)
        elif y is None: #we can have situation of x being not None and y being None 
        #if we input only argument for x; we do either elif y is None or if y is None and x is not None
            self.y=np.random.random(n)
        else:
            self.x=x
            self.y=y
    
def init_config(cities): #!!! WE MAKE INITIAL CONFIGURATION A FUNCTION OUTSIDE OF
#THE CLASS CITIES, CITIES HAVE NO ATTRIBUTE CONFIGURATION
    n=cities.n
    route=np.random.permutation(n)
    return route

def display(cities, route): #!!! route argument indicates the order at which we connect the coordinates, 
#route corresponds to a given permutation of cities, it is the permutation of cities indices
    x, y=cities.x, cities.y
    plt.clf()
    x_ordered=x[route] #indexing using another array
    y_ordered=y[route]
    plt.plot(x, y, "o", color="red") #plotting single points
    plt.plot(x_ordered, y_ordered, color="red") 
    plt.plot([x_ordered[0], x_ordered[-1]], [y_ordered[0], y_ordered[-1]], color="red")
    plt.pause(0.01)
    
    
    
def propose_move(route): #propose_move is the function of route as it
#gives the order of permutation, so it is not a function of cities as the move 
#proposal is quite random, it does not consider cost
    n=np.size(route)
    #e1=np.random.randint(n) #!!! you do not generate just once, you want to 
    #keep generating random numbers as long as condition is met
    #e2=np.random.randint(n)
    while True:
        e1=np.random.randint(n)
        e2=np.random.randint(n)
        if e1>e2:
            e1, e2=e2, e1
        if e2!=e1+1 and e2%(n-1)!=e1: #we do not want to swap neighbouring edges nor the same edge with itself
        #since the configuration is a cycle, 0 and last are neighbours
        #e2%(n-1)!=e1 avoids swapping the same node and first with last
        #e2!=e1+1 avoids swapping neighbouring nodes
            break
    return (e1, e2)

#!!! PROFESSOR DID:
    #route1 = route.copy()
    #route1[e1+1:e2+1] = route[e2:e1:-1]
    #return route1
#SO IN HIS SOLUTION, propose_move returns new route and then delta_cost function
#computes the difference between the costs of 2 routes.
#I however return the concrete move and then compute the cost of difference of the 
#old pair of edges and the new pair of edges
#I managed to compute cost difference without computing total cost of route1, not
#even introducing route1
#PROF MADE ROUTE1 A COPY OF ROUTE, EXPLICITLY, BECAUSE IF ROUTE1 IS A VIEW,
#MODIFICATIONS TO ROUTE1 AFFECT ORIGINAL ROUTE


     
def accept_move(route, move): #DOES IT WORK?
    e1, e2=move
    route[e1+1:e2+1]=route[e2:e1:-1]
    #return route
#swapping means connecting the first node of e1 to the first node of e2 and the second node of e1 to the second node of e2

def distance(cities, city1, city2):
    return np.sqrt((cities.x[city1]-cities.x[city2])**2+(cities.y[city1]-cities.y[city2])**2)

'''
    #coordinates of node1
    x1=cities.x[node1]
    y2=cities.y[node1]
    x2=cities.x[node2]
    y2=cities.y[node2]
'''
    
    
#We can just deal with the function cost_difference, but we may want to know
#the total cost and then upon accepting move updating it by the cost difference.
    
#it is a matter of just labels what we name as a first edge and what as the last
#but the relative labelling of edges must be all right, i.e. correspond do the
#configuration in the right order

def cost_difference(cities, move, route): #length of e1+length of e2 vs length of 2 new edges
    e1, e2=move
    n=cities.n
    v1e1=route[e1] #vertex 1 of edge e1
    v2e1=route[(e1+1)%n] #vertex 2 of edge e1; why do we have to write %n although
    #we have a guarantee that e1 is edge previous to e2 so it shouldn't go out of bounds
    v1e2=route[e2] #vertex 1 of edge e2
    v2e2=route[(e2+1)%n] #vertex 2 of edge e2
    cost_old_edges=distance(cities, v1e1, v2e1)+distance(cities, v1e2, v2e2)
    cost_new_edges=distance(cities, v1e1, v1e2)+distance(cities, v2e1, v2e2)
    return cost_new_edges-cost_old_edges

def total_cost(cities, route):
    n=cities.n
    cost=0
    for i in range(n):
        cost+=distance(cities, route[i], route[(i+1)%n]) #%!!! route[(i+1)%n, 
    #not %(n-1), last i is n-1, while last i+1 is n and since n is out of bounds, we take n%n=0
    #and at the same time i=n-1 so this is the distance between the last and first, completing the cycle
    return cost
               

#we have as input a particular initial configuration of cities
#and the idea of this algorithm is to search for two nodes (propose the move)
#and accept the move if it improves the situation, i.e. if it reduces cost
#pick start

def greedy2(cities, n_iter=10, n_restarts=10, seed=None): 
    if seed is None:
        np.random.seed(seed)
        
    #best_route_global=init_config(cities)
    #best_cost_global=total_cost(cities, best_route_global)
    #display(cities, best_route_global)
    best_route_global=None #proper initialization
    best_cost_global=np.inf
    
    
    print(f"Initial cost is {best_cost_global}.")
    print(f"Initial configuration is {best_route_global}.")
    for j in range(n_restarts):
        route=init_config(cities)
        #display(cities, route)
        cost=total_cost(cities, route)
        for i in range(n_iter):
            move=propose_move(route) 
            print(move)
            delta_cost=cost_difference(cities, move, route)
            print(delta_cost)
            if delta_cost<=0:
                accept_move(route, move) #!!! in my algorithm I am modifying
                #in-place instead of creating a copy of the route, modifying 
                #the copy and assigning it to the original route
                cost+=delta_cost
                #display(cities, route)
        if cost<=best_cost_global:
            best_cost_global=cost
            best_route_global=route
            print(f"Current cost is {best_cost_global}")
            print(f"Current configuration is {best_route_global}.")
            display(cities, best_route_global)
            
    display(cities, best_route_global)
    print(f"Final cost is {best_cost_global}.")
    print(f"Final configuration is {best_route_global}.")
    return best_route_global, best_cost_global
    