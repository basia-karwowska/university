import numpy as np


class GDResults:
    def __init__(self, x_fin, val_fin, n_iters, converged, xs):
        self.x_fin, self.val_fin, self.n_iters, self.converged, self.xs=\
        x_fin, val_fin, n_iters, converged, xs
    def __repr__(self):
        return "Final x: " +str(self.x_fin)+"\n"+"Final f(x): "+str(self.val_fin)+"\n"+"Number of iterations: "+str(self.n_iters)+"\n"+"Convergence: "+str(self.converged)
    #repr method returns string!!!

def grad(f, x, delta = 1e-5):
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
   

def grad_desc(f, x0,
              grad_f = None,
              max_t = 100,
              alpha = 0.01,
              epsilon = 1e-6,
              callback = None, 
              verbosity=0,
              keep_intermediate=False):
    if grad_f is None:
        grad_f = lambda xx: grad(f, xx)
    x = x0
    if keep_intermediate:
        xs = [x0.copy()]
    if not keep_intermediate:
        xs=[]
    converged = False
    for k in range(max_t):
        p = grad_f(x)
        assert len(p) == len(x)
        if keep_intermediate:
            x = x - alpha * p
            xs.append(x)
        if not keep_intermediate:
            x-=alpha*p
        if verbosity>=2:
            print(f"It is {k}th iteration, the current value of x is {x}, of f(x) is {f(x)}, the gradient is {p} and of the gradient norm is {norm(p)}.")
        if callback is not None:
            if callback(x):
                break
        if norm(p) < epsilon:
            converged = True
            print("The optimization suceeded!")
            break
    xs = np.array(xs)
    res=GDResults(x, f(x), k, converged, xs)
    if verbosity>=1:
        print(res)
    return res

