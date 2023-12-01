import numpy as np

def grad(f, x, delta = 1e-5):
    return (f(x + delta) - f(x - delta)) / (2 * delta)

def g(x):
    return x**4 + 4 * x**3 + x**2 - 10 * x + 1

def grad_g(x):
    return 4*x**3+12*x**2+2*x-10

#1.1 We appy grad function to analytical expression to first derivative of g to get
#the second derivative of g.

#we do not reproduce finite differences but we are using grad function which
#we already programmed

def grad2_naive1(g, x, delta = 1e-5): #or g is already first derivative
    gf=lambda x: grad_g(x)
    return grad(gf, x, delta) #(gf(x + delta) - gf(x - delta)) / (2 * delta)

#!!! this is what we were asked to do:
def grad2_naive11(grad_g, x, delta=1e-5):
    return grad(grad_g, x, delta) #(grad_g(x + delta) - grad_g(x - delta)) / (2 * delta)

'''
def grad2_naive1_(x, delta=1e-5):
    return ((4*(x+delta)**3+12*(x+delta)**2+2*(x+delta)-10)-(4*(x-delta)**3+12*(x-delta)**2+2*(x-delta)-10))/(2*delta)
'''


def grad2_naive2(f, x, delta1=1e-5):
    gf=lambda x: grad(f, x, delta1) #!!! lambda function of x!! not of f
    #as then we output grad(gf, x, delta)
    return grad(gf, x, delta=delta1)

'''
def grad2(f, x, delta=1e-5):
    f1=f(x + delta*x + delta * (x + delta*x))
    f2=f(x-x*delta**2)
    f3=f(x-delta*x-delta*(x-delta*x))
    gf1=(f1-f2)/(2*delta*(x+delta*x))
    gf2=(f2-f3)/(2*delta*(x-delta*x))
    gg=(gf1-gf2)/(2*delta*x)
    return gg
'''
def grad2(f, x, delta = 1e-5):
    return (f(x + 2 * delta) - 2 * f(x) + f(x - 2 * delta)) / (4 * delta**2)


def grad2_g(x):
    return 12*x**2+24*x+2
    
def optimal_delta_grad1(f, grad_a, grad_ls, x=0, delta=1e-5):
    grad_a=grad_g(x)
    grad_ls=lambda delta: grad(f, x, delta)
    diff_old=np.inf
    diff_new=abs(grad_a-grad_ls(delta))
    while diff_new<=diff_old:
        delta/=5
        diff_old=diff_new
        diff_new=abs(grad_a-grad_ls(delta))
    return delta*5
    

np.random.seed(100)
x=np.random.randint(1, 10)
differences1=np.zeros(20)
grad_analytical=grad_g(x)
deltas=np.linspace(1e-1, 1e-10, 20)
i=0
for delta in deltas:
    differences1[i]=abs(grad_analytical-grad(g, x, delta))
    i+=1
min_error=np.min(differences1)
delta_opt=deltas[np.argmin(differences1)]
print(f"Minimum error for grad1 is {min_error}, which occurs for delta equal to {delta_opt}")
    
#def optimal_delta_grad2
    
np.random.seed(100)
y=np.random.randint(1, 10)
differences2=np.zeros(20)
grad_analytical2=grad2_g(x)
deltas2=np.linspace(1e-1, 1e-10, 20)
j=0
for delta2 in deltas2:
    differences2[j]=abs(grad_analytical2-grad2(g, y, delta2))
    j+=1
min_error2=np.min(differences2)
delta_opt2=deltas2[np.argmin(differences2)]
print(f"Minimum error for grad2 is {min_error2}, which occurs for delta equal to {delta_opt2}")
    





