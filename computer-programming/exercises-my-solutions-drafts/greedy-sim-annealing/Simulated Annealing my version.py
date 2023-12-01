import TSP
import numpy as np

#accept function returns info whether the move is accepted, does not include acceptance
#method but if accept function returns True, acceptance method is applied

def accept(delta, beta): #only depends on delta beta, probability includes these terms
    if delta<=0:
        return True
    if delta==np.inf:
        return False
    else:
        p=np.exp(-beta*delta)
        return np.random.random()<p #np.random.random() generates numbers
#from 0 to 1 from a uniform distribution, therefore the probability of being
#below p is p, p is also a probability of obtaining 1 from the binomial dist
#see that expected values are the same in both cases

'''
def accept(problem, move, beta):
    delta=problem.delta_cost(move)
    if delta<=0:
        problem.accept_move(move)
        return True
    if delta==np.inf:
        return False
    else:
        prob=np.exp(-beta*delta)
        decision=np.random.binomial(1, prob)
        if decision==True:
            problem.accept_move(move)
            return True
    return False
'''
            
#methods are generic so we will exploit them


def simulated_annealing(problem, mcmc_iters=1000, beta0=1., beta1=100., anneal_steps=10, seed=None): # maybe the order should be a bit differen, previously you wrote: 
    #(problem, beta_first, beta_penultimate, n_betas, n_iter=100)
    #we need to tune by adjusting the number of mcmc_iters based on the 
    #variations in cost for different trials and betas based on acceptance rate
    if seed is not None:
        np.random.seed(seed)
    
    best_problem=None
    best_cost=np.inf
    
    #betas=np.logspace(beta0, beta1, anneal_steps)
    #beta_last=np.inf
    #beta_list=np.append(betas, beta_last)
    
    
    #MAYBE MORE EFFICIENT INSTEAD OF APPENDING:
    beta_list = np.zeros(anneal_steps) #container and filling contents of the list
    beta_list[:-1] = np.logspace(np.log10(beta0), np.log10(beta1), anneal_steps-1)
    beta_list[-1] = np.inf
    
    #WE INITIALIZE THE PROBLEM
    problem.init_config() #we call it here, not within the loop because we want
    #to start each time from the configuration we were left off
    #and in simulated annealing we do not have restarts
    cost=problem.cost()
    
    #n_runs=(n_betas+1)*n_iter
    
    for beta in beta_list:
        n_acceptance=0
        for i in range(mcmc_iters): 
            move=problem.propose_move() #assuming symmetric, this way we constructed acceptance
            delta=problem.delta_cost(move)
            if accept(delta, beta):
                cost+=delta
                problem.accept_move(move)
                n_acceptance+=1 #acceptance rate gives useful insights whether to tune
                
                #BETTER to indent this because then it only evaluates this if-statement if
                #the move is accepted, it is not a mistake I believe, but wastes the cost if 
                #we evaluate it regardless
                
                if cost<=best_cost:
                    best_cost=cost
                    best_problem=problem.copy()
        print(f"Acceptance rate for beta={beta} is {n_acceptance/mcmc_iters}.")
    print(f"best score = {best_cost}")
    best_problem.display()
    return best_problem
            