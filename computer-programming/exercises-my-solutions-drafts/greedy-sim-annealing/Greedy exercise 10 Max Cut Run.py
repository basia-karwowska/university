from Greedy_exercise_10_Max_Cut import MaxCut
import SimAnn
# import numpy as np
'''
mxc = MaxCut(50, seed=678678)

best = SimAnn.simann(mxc, mcmc_steps=10**4, seed=58473625,
                     beta0=0.1, beta1=10.0, anneal_steps=20)

m=MaxCut(9)
best2=SimAnn.simann(mxc, mcmc_steps=10**4, seed=58473625,
                     beta0=0.1, beta1=10.0, anneal_steps=20)
'''

n=MaxCut(5)
best3=SimAnn.simann(n, mcmc_steps=10**4, seed=58473625,
                     beta0=0.1, beta1=10.0, anneal_steps=20)