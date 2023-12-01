#Lecture 3 additional tasks
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy

#%% PLOTTING A QUARTER OF A CIRCLE + MONTE CARLO IN 2D
'''
Technique:
1. Generate a list of points on the circumference of the circle with radius 1.
x-coordinates of such points are given by cos(angle) and y-coordinates by sin(angle)
Angles in the first quadrant can be between 0 and pi/2.
We want evently spaced points so we create an array of evenly spaced numbers 
between 0 and pi/2 using np.linspace and then compute cos and sin of elements of this array.
We gather the results in new arrays.
2. Plot the connected points by passing the arrays into plot function.
What do we do differenty if we want to plot just points and when we want to plot connected points?
'''
n_points=100
theta=np.linspace(0, np.pi/2, n_points) #returns evently spaced numbers over a specified interval

xs=np.zeros(n_points) 
ys=np.zeros(n_points)
for i in range(n_points):
    xs[i]=np.cos(theta[i])
    ys[i]=np.sin(theta[i])
#short version of the code above:
xs=np.cos(theta)
ys=np.sin(theta)
  
plt.plot(xs, ys, color="red")
  
mc_points=150
random_x=np.random.random(mc_points)
random_y=np.random.random(mc_points)
    

plt.plot([[0, 0], [1, 1], [0, 1], [0, 1]], [[0, 1], [0, 1], [0, 0], [1, 1]], color="black", linestyle="dashed")
plt.plot(random_x, random_y, "o", color="red")



#MONTE CARLO IN 2D



ninside=0
for i in range(mc_points):
    if (random_x[i])**2+(random_y[i])**2<1:
        ninside+=1 
print(f"mc.pi estimation (2-dimensional case)={4*(ninside/mc_points)}, pi={np.pi}")


#%% SCALING, STANDARD DEVIATION

#for two dimensions, how std deviation varies as we increase n_points
def scaling_mc(n_samples=5, n_repet=50):
     sd=np.zeros(n_samples)
     for i in range(n_samples):
         n_points=10**(i+1) #better to do here i+1 than change it in range()
         #in order to avoid out of bounds error
         pi_estimations=np.zeros(n_repet)
         for j in range(n_repet): #number of repetition for every number of points
             rand_x=np.random.random(n_points)
             rand_y=np.random.random(n_points)
             n_inside=0
             for k in range(n_points):
                 if (rand_x[k])**2+(rand_y[k])**2<=1:
                     n_inside+=1
             pi_estimation=4*n_inside/n_points
             pi_estimations[j]=pi_estimation
         std_dev=np.std(pi_estimations)
         sd[i]=std_dev
     return sd
 
#AS THE DIMENSIONS CHANGE:
def scaling_mc_2(n_dimensions=5, n_repet=50, n_points_=500):
    sd=np.zeros(n_dimensions)
    for i in range(n_dimensions):
        dim=i+2
        pi_estimations=np.zeros(n_repet)
        for j in range(n_repet): 
            pi_estimations[j]=mc_pi_estimator(dim, n_points_)
        sd[i]=np.std(pi_estimations)
    return sd

'''
def scaling_mc2(n_dimensions=5, n_repet=50, n_points_):
     sd=np.zeros(n_dimensions)
     for i in range(n_dimensions):
         dim=i+2
         pi_estimations=np.zeros(n_repet)
         for j in range(n_repet): #number of repetition for every number of points
             random_array_=np.random.random(dim, n_points_)
             n_inside=(random_array_.sum(axis=0)<1).sum()
             
             pi_estimation=4*n_inside/n_points_
             pi_estimations[j]=pi_estimation
         std_dev=np.std(pi_estimations)
         sd[i]=std_dev
     return sd
        
''' 
    
#%% MC IN 3 DIMENSIONS

#Imagine an eight of the sphere placed in a unit cube, consider points falling
#inside of the eight of the sphere vs points falling outside, compute the ratio
#of points inside vs total points

number_points=150
x_rand=np.random.random(number_points) 
y_rand=np.random.random(number_points)
z_rand=np.random.random(number_points)
number_inside=0
for i in range(number_points):
    if (x_rand[i])**2+(y_rand[i])**2+(z_rand[i])**2<=1:
        number_inside+=1
print(f"mc.pi estimation (3-dimensional case)={6*(number_inside/number_points)}, pi={np.pi}")
#1/8*4/3*pi*r^3/r^3=1/6*pi
    

#%% MC IN ANY DIMENSIONS
def mc_pi_estimator(dim, n_p=150): 
    arrays_collection=np.zeros((dim, n_p))
    for i in range(dim):
        arrays_collection[i]=np.random.random(n_p) #arrays_collection[i], not arrays_collection[dim]!
    inside=0
    for p in range(n_p):
        norm_squared=0
        for a in range(dim):
            norm_squared+=arrays_collection[a][p]**2
        if norm_squared<=1:
            inside+=1
    #pi_estimation=(inside*2**dim*math.factorial(dim/2)/n_p)**(2/dim)
    pi_estimation=(inside*2**dim*scipy.special.gamma(dim/2+1)/n_p)**(2/dim)
    #print(f"mc.pi estimation ({dim}-dimensional case)={pi_estimation}, pi={np.pi}")
#1/8*4/3*pi*r^3/r^3=1/6*pi
    return pi_estimation
    


def estimator_pi(n, dim=2):
    random_array=(np.random.random((dim, n)))**2
    ninsidee=0
    for i in range(n):
        if random_array.sum(axis=0)[i]<1:
            ninsidee+=1
    pi_estimation=(ninsidee/n*2**dim*scipy.special.gamma(dim/2+1))**(2/dim)
    print(f"mc.pi estimation ({dim}-dimensional case)={pi_estimation}, pi={np.pi}")
    
        




        