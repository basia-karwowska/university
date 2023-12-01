import numpy as np
import matplotlib.pyplot as plt
roots=np.array([1.5+0j, -1+2j, -1-2j])
def f(z):
    return (z-roots[0])*(z-roots[1])*(z-roots[2]) #degree 3 polynomial in the complex plane

#Newton's method
def fp(z):
    return (z-roots[0])*(z-roots[1])+(z-roots[1])(z-roots[2])+(z-roots[0])(z-roots[2])

list_complex=np.zeros(5, dtype=complex)

def newtons_update(z):
    return z-f(z)/fp(z)
#z=... #we are overwriting
z=f(z)
z=newtons_update(z) #we keep doing until we reach convergence so value 0

def run_newton(n=1000, n_steps=10):
    z=np.zeros((n, n), dtype=complex)
    interval=np.linspace(-5, 5, n)
    z.real, z.imag=np.meshgrid(interval, interval)
    #we are starting with the cloud of points but around the roots, there will be
    #convergence
    #updating element-wise with Newton's method
    for t in range(n_steps):
        z[:]=newtons_update(z)
        
    #we are looking at the distance between z and roots
    #which one is the smallest
    dist=[np.abs(z-roots[k]) for k in range(3)]
    closer_root=np.argmax(dist, axis=0)
    plt.clf()
    plt.imshow(closer_root)
    #1 step - points converging unless we are in a critical region, then jumping from 1 to another
    #all points in the green region converge to 1 root, consider the boundary
    #points close to the boundary
    #boundaries - the number of colors like the number of roots so we get a 
    #fractal structure, all colors must be on the boundary
    #Newton's fractal
    return z
    
    #both in x and y directions
    #we are treating real and imaginary part as x and y coordinates
    #matrix of complex numbers