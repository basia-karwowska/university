from scipy.optimize import minimize
from function_examples import k, g
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from GradDescExercise5 import grad

#1) First we experiment with varied optimization methods, we will use
#Nelder-Mead, Powell, CG, BFGS, Newton-CG and compare the respective trajectories.

#%% Function g

z0g=np.array([-2, -0.5]) #initial guess for the minimizer of g, common for all optimization methods that we will test

#Different optimization methods:
    
#Contour plot to visualize and compare minimize trajectories for various optimization methods. Setup:
    
plt.close("all")
plt.figure()    
plt.title("Minimize trajectories for function g")   
#we decided on range of x_coord and y_coord by inspecting the value of the optimum
#which we determined to be around [-1.83333335, -0.33333334] and initial guess [-2, -0.5]
#we want to be able to visualize the entire trajectory and we know that the direction
#is towards the minimum so we just want to make sure that both the minimum and initial
#guess are within the bounds of our grid           
x_coord = np.linspace(-2.5, -1.0, 1000)
y_coord = np.linspace(-0.8, 0.0, 1000)
x_coord, y_coord = np.meshgrid(x_coord, y_coord)
z_coord = g(np.stack((x_coord, y_coord))) 
plt.contour(x_coord, y_coord, z_coord, 50, cmap='RdGy')

#1. Nelder-Mead
min_zs_g_1 = [z0g]
res_g_1 = minimize(g, z0g, method="Nelder-Mead", callback = lambda xg: min_zs_g_1.append(xg))
min_zs_g_1 = np.array(min_zs_g_1)
plt.plot(min_zs_g_1[:,0], min_zs_g_1[:,1], 'x-', color="red", label="Nelder-Mead")
print(f"Number of iterative steps until convergence is {res_g_1.nit}")

#2. Powell
min_zs_g_2 = [z0g]
res_g_2 = minimize(g, z0g, method="Powell", callback = lambda xg: min_zs_g_2.append(xg))
min_zs_g_2 = np.array(min_zs_g_2)
plt.plot(min_zs_g_2[:,0], min_zs_g_2[:,1], 'x-', color="blue", label="Powell")
print(f"Number of iterative steps until convergence is {res_g_2.nit}")

#3. CG
min_zs_g_3 = [z0g]
res_g_3 = minimize(g, z0g, method="CG", callback = lambda xg: min_zs_g_3.append(xg))
min_zs_g_3 = np.array(min_zs_g_3)
plt.plot(min_zs_g_3[:,0], min_zs_g_3[:,1], 'x-', color="green", label="CG")
print(f"Number of iterative steps until convergence is {res_g_3.nit}")

#4. BFGS
min_zs_g_4 = [z0g]
res_g_4 = minimize(g, z0g, method="BFGS", callback = lambda xg: min_zs_g_4.append(xg))
min_zs_g_4 = np.array(min_zs_g_4)
plt.plot(min_zs_g_4[:,0], min_zs_g_4[:,1], 'x-', color="black", label="BFGS")
print(f"Number of iterative steps until convergence is {res_g_4.nit}")

#5. Newton-CG
min_zs_g_5 = [z0g]
#jacobian is required for Newton-CG (for us Jacobian is a gradient as we are working
#on 1-dimensional ndarray i.e. on vectors, not matrices as inputs)
res_g_5 = minimize(g, z0g, method="Newton-CG", jac=lambda xx: grad(g, xx), callback = lambda xg: min_zs_g_5.append(xg))
min_zs_g_5 = np.array(min_zs_g_5)
plt.plot(min_zs_g_5[:,0], min_zs_g_5[:,1], 'x-', color="orange", label="Newton-CG")
print(f"Number of iterative steps until convergence is {res_g_5.nit}")


#%% Function k

z0k = np.array([0.5, -1.0])

plt.figure() 
plt.title("Minimize trajectories for function g")            
x_coord2 = np.linspace(-0.4, 1, 1000) #seeing some empty white space without the
#contour lines, we need to fix it and adjust the range x_coord2 accordingly
y_coord2 = np.linspace(-1, 1, 1000)
x_coord2, y_coord2 = np.meshgrid(x_coord2, y_coord2)
z_coord2 = k(np.stack((x_coord2, y_coord2))) 
plt.contour(x_coord2, y_coord2, z_coord2, 50, cmap='PuBu')

#we adjust ranges of x- and y-coordinates to be able to include
#the final minimizer [0.03808639, 0.25206588] and initial guess [0.5, -1.0]

#1. Nelder-Mead
min_zs_k_1 = [z0k]
res_k_1=minimize(k, z0k, method="Nelder-Mead", callback = lambda xk: min_zs_k_1.append(xk))
min_zs_k_1=np.array(min_zs_k_1)
plt.plot(min_zs_k_1[:,0], min_zs_k_1[:,1], 'x-', color="red", label="Nelder-Mead")
print(f"Number of iterative steps until convergence is {res_k_1.nit}.")

#2. Powell
min_zs_k_2 = [z0k]
res_k_2=minimize(k, z0k, method="Powell", callback = lambda xk: min_zs_k_2.append(xk))
min_zs_k_2=np.array(min_zs_k_2)
plt.plot(min_zs_k_2[:,0], min_zs_k_2[:,1], 'x-', color="blue", label="Powell")
print(f"Number of iterative steps until convergence is {res_k_2.nit}")

#3. CG
min_zs_k_3 = [z0k]
res_k_3=minimize(k, z0k, method="CG", callback = lambda xk: min_zs_k_3.append(xk))
min_zs_k_3=np.array(min_zs_k_3)
plt.plot(min_zs_k_3[:,0], min_zs_k_3[:,1], 'x-', color="green", label="CG")
print(f"Number of iterative steps until convergence is {res_k_3.nit}")

#4. BFGS
min_zs_k_4 = [z0k]
res_k_4=minimize(k, z0k, method="BFGS", callback = lambda xk: min_zs_k_4.append(xk))
min_zs_k_4=np.array(min_zs_k_4)
plt.plot(min_zs_k_4[:,0], min_zs_k_4[:,1], 'x-', color="black", label="BFGS")
print(f"Number of iterative steps until convergence is {res_k_4.nit}")

#5. Newton-CG
min_zs_k_5 = [z0k]
res_k_5=minimize(k, z0k, method="Newton-CG", jac=lambda xx: grad(k, xx), callback = lambda xk: min_zs_k_5.append(xk))
min_zs_k_5=np.array(min_zs_k_5)
plt.plot(min_zs_k_5[:,0], min_zs_k_5[:,1], 'x-', color="orange", label="Newton-CG")
print(f"Number of iterative steps until convergence is {res_k_5.nit}")


#Powell and CG give the best results.

#2) Hessian analytical vs grad2 method.

plt.figure()    
plt.title("Hessian analytical vs Hessian estimated using grad2")             
x_coord3 = np.linspace(-2.5, -1.0, 1000)
y_coord3 = np.linspace(-0.8, 0.0, 1000)
x_coord3, y_coord3 = np.meshgrid(x_coord3, y_coord3)
z_coord3 = g(np.stack((x_coord3, y_coord3))) 
plt.contour(x_coord3, y_coord3, z_coord3, 50, cmap='RdGy')

def hessian_analytical_g(x):
    return np.array([[2, -2], [-2, 8]])
#hessian here does not need arguments, it has constant values 
#but since hess is callable we still need to have it in a form of a function while
#pssing it to minimize and we will still need lambda function so you can make it
#a function of some dummy variable
    
min_zs_g_6 = [z0g]
res_g_6 = minimize(g, z0g, method="Newton-CG", jac=lambda xx: grad(g, xx), hess=lambda xx2: hessian_analytical_g(xx2), callback = lambda xg: min_zs_g_6.append(xg))
min_zs_g_6 = np.array(min_zs_g_6)
plt.plot(min_zs_g_6[:,0], min_zs_g_6[:,1], 'x-', color="orange")
print(f"Number of iterative steps until convergence is {res_g_6.nit}")

from GradDescExercise3 import hessian2

min_zs_g_7 = [z0g]
res_g_7 = minimize(g, z0g, method="Newton-CG", jac=lambda xx: grad(g, xx), hess=lambda xx2: hessian2(g, xx2), callback = lambda xg: min_zs_g_7.append(xg))
min_zs_g_7 = np.array(min_zs_g_7)
plt.plot(min_zs_g_7[:,0], min_zs_g_7[:,1], 'x-', color="red")
print(f"Number of iterative steps until convergence is {res_g_7.nit}")

#Basically it is the same whether we use hessian estimation using grad2 or analytical
#the trajectories lie on top of one another.

#3) Constrained optimization - introducing bounds!
#We will consider the bounds for the Powell method of minimize applied to g.
#Bounds will be [0, 3] x [1, 2]
#!!! We adapt ranges for x_coord and y_coord so that they include the optimal solution
#without bounds and the entire region bounded by bounds (we want to draw a square
#so want to have linspace wider than bounds ofc) because we want to compare
#the result with and without bounds. Initial guess must be within bounds.

#can initial guess be not within bounds? (recall z0g=np.array([-2, -0.5]))
fig, ax=plt.subplots()    
plt.title("Optimization with and without bounds")  
rect=Rectangle((0, 1), 3, 1, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)   
x_coord4 = np.linspace(-2.5, 5, 1000)
y_coord4 = np.linspace(-1, 3, 1000)
x_coord4, y_coord4 = np.meshgrid(x_coord4, y_coord4)
z_coord4 = g(np.stack((x_coord4, y_coord4))) 
plt.contour(x_coord4, y_coord4, z_coord4, 50, cmap='RdGy')

z0g_b=np.array([1.5, 1.5])

min_zs_g_8 = [z0g_b]
res_g_8 = minimize(g, z0g_b, method="Powell", bounds=[(0, 3), (1, 2)], callback = lambda xg: min_zs_g_8.append(xg))
min_zs_g_8 = np.array(min_zs_g_8)
plt.plot(min_zs_g_8[:,0], min_zs_g_8[:,1], 'x-', color="blue")

#Without bounds, we already computed so we exploit the result to plot it:
plt.plot(min_zs_g_2[:,0], min_zs_g_2[:,1], 'x-', color="black")

#Without bounds but with initial guess equal to the one which we guessed in the
#presence of bounds.

min_zs_g_9 = [z0g_b]
res_g_9 = minimize(g, z0g_b, method="Powell", callback = lambda xg: min_zs_g_9.append(xg))
min_zs_g_9 = np.array(min_zs_g_9)
plt.plot(min_zs_g_9[:,0], min_zs_g_9[:,1], 'x-', color="red")


#it ends up in the actual value

#4) For k with Nelder-Mead method we needed 43 steps to converge to the optimal solution.
#Let's restrict the number of iterative steps to 30 and see what value we get.
#We can compare it with the optimum to which the minimize function converges
#when there is no limit defined by us on this number of steps.
min_zs_k_6=[z0k]
res_k_6=minimize(k, z0k, method="Nelder-Mead", callback = lambda xk: min_zs_k_6.append(xk), options={"maxiter" : 30})
#options={"maxiter" : 30} ==> dictionary of options, keys are strings!
print(f"The minimum value when maxiter=30 is {res_k_6.fun}, while when the number of iterations is not limited it is {res_k_1.fun}.")
print(f"The corresponding arguments to which minimizer using the Nelder-Mead method converges is {res_k_6.x} and {res_k_1.x}.")


#how to change to usual norm instead of infinite norm? specify tolerance in a proper way!

#5) 2-norm vs infinite norm
min_zs_k_7=[z0k]
res_k_7=minimize(k, z0k, method="BFGS", callback = lambda xk: min_zs_k_7.append(xk), options={"norm" : 2})
print(f"The minimum value when the 2-norm is used {res_k_7.fun}, while when the inf-norm is used is {res_k_4.fun} (BFGS method applied to k).")
print(f"The corresponding arguments to which minimizer converges are {res_k_7.x} and {res_k_4.x}.")
