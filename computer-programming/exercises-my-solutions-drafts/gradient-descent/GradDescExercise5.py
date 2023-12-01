import numpy as np


class GDResults:
    def __init__(self, x_fin, val_fin, n_iters, converged, xs):
        self.x_fin, self.val_fin, self.n_iters, self.converged, self.xs=\
        x_fin, val_fin, n_iters, converged, xs
    def __repr__(self):
        return "Final x: " +str(self.x_fin)+"\n"+"Final f(x): "+str(self.val_fin)+"\n"+"Number of iterations: "+str(self.n_iters)+"\n"+"Convergence: "+str(self.converged)
    #repr method returns string!!!

def grad(f, x, delta = 1e-3):
    n = len(x)
    g = np.zeros(n)                         
    for i in range(n):                      
        x_old = x[i]
        x[i] = x_old + delta
        fp = f(x)                          
        x[i] = x_old - delta
        fm = f(x)                          
        x[i] = x_old
        g[i] = (fp - fm) / (2 * delta)
    return g



def norm(x):
    return np.sqrt(np.sum(x**2))
   
def norm_inf(x):
    return np.min(abs(x))

def grad_desc(f, x0,
              grad_f = None,
              max_t = 100,
              alpha = 0.01,
              epsilon = 1e-6,
              callback = None, 
              verbosity=0,
              keep_intermediate=False, 
              beta=0, norm_type="standard"): #beta=0 coincides with Nesterov being false
#norm_type="standard" or norm_type="infinite"; write norm_type and not norm because
#then the local definition of norm will take precedence over global function and then
#it would get overwritten, we should not have the same names
    if grad_f is None:
        grad_f = lambda xx: grad(f, xx)
    x = x0.copy() #!!! safer to have a copy
    xs=[] #initialize here
    if keep_intermediate:
        xs.append(x0.copy()) #you could also do xs=[x0.copy()] but appending is
        #better so that you keep old object and not overwrite all the time
    #if not keep_intermediate: #just initialize xs at the beginning!!
        #xs=[]
    converged = False
    v=np.zeros(len(x0))
    for k in range(max_t):
        p = grad_f(x+beta*v) #Nesterov momentum, gradient in a shifted position
        #(or current if beta=0)
        v = beta*v-alpha*p
        assert len(p) == len(v) == len(x)
        if keep_intermediate:
            x = x + v
            xs.append(x)
        if not keep_intermediate:
            x+=v #i wanted to try but idk if it works always
            #x+=v
            #np.add(x, v, out=x, casting="unsafe") #!!! I made it like that because I got a message
            #Cannot cast ufunc 'add' output from dtype('float64') to dtype('int32') with casting rule 'same_kind'
        if verbosity>=2:
            print(f"It is {k}th iteration, the current value of x is {x}, of f(x) is {f(x)}, the gradient is {p} and of the gradient norm is {norm(p)}.")
        if callback is not None:
            if callback(x):
                break
        if norm_type=="standard":
            if norm(p) < epsilon:
                converged = True
            #print("The optimization suceeded!")
                break
        if norm_type=="infinity":
            if norm_inf(p)<epsilon:
                converged = True
                break
    xs = np.array(xs)
    res=GDResults(x, f(x), k+1, converged, xs)
    if verbosity>=1:
        print(res)
    return res

from function_examples import g, k
res111=grad_desc(g, [-3, 1])
ress111=grad_desc(k, [-5, 5], max_t=200)
from scipy.optimize import minimize
resss111=minimize(g, [-3, 1])
ressss111=minimize(k, [-5, 5])