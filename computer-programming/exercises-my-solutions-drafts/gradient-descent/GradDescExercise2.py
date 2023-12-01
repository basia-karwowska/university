# -*- coding: utf-8 -*-
import numpy as np
from scipy.special import binom

def g(x):
    return x**4 + 4 * x**3 + x**2 - 10 * x + 1

def grad_g(x):
    return 4 * x**3 + 12 * x**2 + 2 * x - 10

def grad2_g(x):
    return 12 * x**2 + 24 * x + 2

def grad3_g(x):
    return 24 * x + 24

def grad4_g(x):
    return 24.0


def grad(f, x, delta = 1e-5):
    return (f(x + delta) - f(x - delta)) / (2 * delta)


def grad3_naive1(grad_2, x, delta=1e-5):
    return grad(grad_2, x, delta)

def grad3_naive2(f, x, delta=1e-5):
    gf=lambda x: grad(f, x, delta)
    gf2=lambda x: grad(gf, x, delta)
    return grad(gf2, x, delta)

def grad3_(f, x, delta=1e-5):
    return (f(x+3*delta)-3*f(x+delta)+3*f(x-delta)-f(x-3*delta))/(8*delta**3)


def grad3_naive222(f, x, delta = 1e-4):
    gf = lambda x: grad(f, x, delta)
    gf2 = lambda x: grad(gf, x, delta)
    return grad(gf2, x, delta)

### this one is the simplified finite-differences expression, the analog of `grad2`
def grad333(f, x, delta = 1e-3):
    return (f(x + 3 * delta) - 3 * f(x + delta) + 3 * f(x - delta) - f(x - 3 * delta)) / (8 * delta**3)

# pay attention to approximations
x=10
true_value=grad3_g(x)
err1=grad3_naive1(grad2_g, x, 1e-3)-true_value
err2=grad3_naive2(g, x, 1e-3)-true_value
err3=grad3_(g, x, 1e-3)-true_value

#grad_naive1 has the smallest error but it is not so efficient, while grad3_
#which is way more efficient has also greater error
print(f"True value is {true_value}; Error for grad3_naive1 is {err1}, for grad3_naive2 is {err2} and for grad3_ is {err3}.")


i=0
def gradn(n, f, x, delta=1e-5):
    global i   
    i+=1
    if n==0:
        return f(x)
    else:
        print(i)
        return grad(lambda x: gradn(n-1, f, x, delta), x, delta)
    
    

def grad_multi(n, f, x, delta=1e-3):
    numerator=0.0
    prefactor=1
    for i in range(n+1):
        numerator+=prefactor*binom(n, i)*f(x+(n-2*i)*delta)
        print(f"numerator is now {numerator}")
        prefactor*=(-1)
        print(f"prefactor is now {prefactor}")
    #broadcasting
    prefactors=-np.ones(n+1)
    print(f"prefactors are {prefactors}")
    prefactors[::2]=1
    print(f"prefactors now are {prefactors}")
    coefficients=binom(n, np.arange(n+1))
    print(f"coefficients are {coefficients}")
    functions=f(x+(n-2*np.arange(n+1))*delta)
    print(f"functions are now {functions}")
    num=prefactors*coefficients*functions
    res=num.sum()/(2*delta)**n
    print(f"num is {num}, res is {res}")
    return numerator/(2*delta)**n, res
        
        
        

    