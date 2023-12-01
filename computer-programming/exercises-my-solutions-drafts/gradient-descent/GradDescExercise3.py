import numpy as np
#Hessian: a square matrix of second-order partial derivatives of a scalar-valued function, or scalar field.
#f takes an array, a vector as an input, arguments=[x1, x2, x3, ..., xn]

def g(args):
    return args[0]**2+2*args[0]*args[1]+args[1]**3

def hessian(f, args, delta=1e-3):
    n=len(args)
    h=np.zeros((n, n))
    delta_i=np.zeros(n)
    delta_j=np.zeros(n)
    for i in range(n): #first we fill out rows
        delta_i[i]=delta
        for j in range(n):
            delta_j[j]=delta
            h[i, j]=(f(args+delta_i+delta_j)-f(args+delta_i-delta_j)-f(args-delta_i+delta_j)+f(args-delta_i-delta_j))
            delta_j[j]=0 #back to previous state
        delta_i[i]=0 #back to previous state
    h/=4*delta**2
    return h
    
    
def hessian2(f, args, delta=1e-5):
    n=len(args)
    h=np.zeros((n, n))
    for i in range(n):
        args_i_old=args[i]
        for j in range(n):
            #args_old=args #we cannot store args in args_old because args is
            #mutable and this is a view, it will get mutated when we change args[i]
            #also it is not efficient to store an entire array (for example by
            #doing args_old=args.copy()), we could instead store x_i_old and
            #x_j_old at each iteration as these are immutable and then we want
            #to return to our old args without approximation errors (we could
            #also add/subtract back delta but that may give rise to some approximation
            #issues)
            
            args_j_old=args[j]
            
            args[i]+=delta
            args[j]+=delta
            fpp=f(args) #first term fpp stands for f plus flus, meaning
            #it is f(x+delta_i+delta_j) in notes
            #for fpm args[i] stays the same while we change args[j]
            
            args[i]=args_i_old
            args[j]=args_j_old
            args[i]+=delta
            args[j]-=delta
            #args[j]=args_j_old-delta we do not want to assign as this would
            #lead to overwriting in the case of diagonal entries, we want to
            #update by += and -= instead of assigning
            #so we also need to retrieve the old value in each case
            fpm=f(args)
            
            args[i]=args_i_old
            args[j]=args_j_old
            args[i]-=delta
            args[j]+=delta
            fmp=f(args)
            
            args[i]=args_i_old
            args[j]=args_j_old
            args[i]-=delta
            args[j]-=delta
            fmm=f(args)
            
            
            h[i, j]=(fpp-fpm-fmp+fmm)/(4*delta**2) #input right signs!!
            args[i], args[j]=args_i_old, args_j_old
            
            #PAY ATTENTION TO THE DIAGONAL! the version below would not work
            #as in the case of diagonal we could need f(x+2delta_i), f(x), f(x), f(x-2delta_i)
            #and the method below would overwrite args[i]=something, but then
            #when we do args[j]=args_j-old-delta, when i==j, and we would get
            #f(x-delta_j) instead of f(x)
            
            '''
            args_j_old=args[j]
            
            args[i]+=delta
            args[j]+=delta
            fpp=f(args) #first term fpp stands for f plus flus, meaning
            #it is f(x+delta_i+delta_j) in notes
            #for fpm args[i] stays the same while we change args[j]
    
            args[j]=args_j_old-delta
            fpm=f(args)
            
            args[i]=args_i_old-delta
            args[j]=args_j_old+delta
            fmp=f(args)
            
            args[j]=args_j_old-delta
            fmm=f(args)
            
            
            h[i, j]=(fpp+fpm+fmp+fmm)/(4*delta**2)
            args[i], args[j]=args_i_old, args_j_old
            
            #PAY ATTENTION TO THE DIAGONAL!
            '''
    return h
            
            
            
