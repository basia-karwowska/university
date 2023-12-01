import numpy as np
from numpy import random as rnd
import matplotlib.pyplot as plt
#TSP AND GREEDY

#we create a random, generic instance of TSP
class Cities:
    def __init__(self, n, seed=None):
        if not (isinstance(n, int) and n>=4):
            raise Exception("n should be an int larger than 4")
        if seed is not None: #if the same seed, random number generator will
        #generate the same sequence of numbers? in order not to repeat?
        
        #SEED????
            rnd.seed(seed)
        self.n=n
        x=rnd.rand(n)
        y=rnd.rand(n)
        self.x=x #we do not need to write x and y in the bracket of init 
        #x and y can be defined using solely information in self and n
        self.y=y
        
        
#order at which we visit cities, we can take a random permutation in TSP   

def init_config(cities):
    n=cities.n
    route=rnd.permutation(n)
    return route

def display(cities, route):
    x, y=cities.x, cities.y
    plt.clf()
    plt.plot(x, y, "o") #with no optional arguments, it will produce a graph with
    #points connected to their successive points
    city1=route[0]
    city2=route[1]
    #plt.plot([x[city1], x[city2]], [y[city1], y[city2]], "-", c="orange")
    plt.plot(x[route], y[route], "-", c="orange")
    comeback=[route[-1], route[0]]
    plt.plot(x[comeback], y[comeback], "-", c="orange")
    return

def propose_move(route): #we are going along the route in order
    n=len(route)
    e1=rnd.randint(n)
    #edge between cities route[e1] and route[e1+1]
    e2=rnd.randint(n)
#How to propose a starting point
#we need to check if we are sensible choices 

#SEED
#In initialization of class Cities: not just creation of the problem is reproducible 
#but also the run of our algorithm is reproducible (seed in definition of greedy())
'''
def greedy(cities, args, seed=None):
    if seed is not None:
        rnd.seed(seed)
    x=init_conf(cities) #function which initializes configuration
    for t in range(num_iters):
        y=propose_move(x) #function which proposes the move
        if cost(y)<=cost(x): #cost function
            #we accept if the cost did not change even or if it got smaller (better)
            x=y
    return x, cost(x)


'''